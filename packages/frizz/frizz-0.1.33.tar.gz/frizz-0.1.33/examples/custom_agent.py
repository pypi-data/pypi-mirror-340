"""
Custom Agent implementation for examples that works with the current aikernel API.

This file provides a modified Agent class that uses the router._completion method directly
instead of relying on the llm_tool_call function which is currently broken.
"""
import json
from collections.abc import Iterator
from contextlib import contextmanager
from functools import cached_property
from typing import Any

import yaml
from aikernel import (
    Conversation,
    LLMAssistantMessage,
    LLMMessagePart,
    LLMModelAlias,
    LLMRouter,
    LLMSystemMessage,
    LLMToolMessage,
    LLMToolMessageFunctionCall,
    LLMUserMessage,
    llm_structured,
)
from pydantic import BaseModel, ValidationError

from frizz._internal.tools import Tool
from frizz._internal.types.response import AgentMessage, StepResult
from frizz._internal.types.system import IGetToolSystemMessagePart
from frizz.errors import FrizzError


class Agent[ContextT]:
    """An AI agent capable of using tools to assist in conversations.
    
    This is a custom implementation that works around the broken llm_tool_call function
    in the aikernel library by directly using the router._completion method.
    
    Type Parameters:
        ContextT: The type of the context object that will be passed to tools.
    """
    def __init__(
        self,
        *,
        tools: list[Tool[ContextT, Any, Any]],
        context: ContextT,
        system_message: LLMSystemMessage | None = None,
        conversation_dump: str | None = None,
        get_tools_system_message_part: IGetToolSystemMessagePart | None = None,
    ) -> None:
        """Initialize a new Agent instance.
        
        Args:
            tools: A list of Tool instances that the agent can use.
            context: Context object passed to tools when they are called.
            system_message: Optional system message to set for the conversation.
            conversation_dump: Optional string dump of a previous conversation to restore.
            get_tools_system_message_part: Optional function to generate system message part for tools.
        """
        self._tools = tools
        self._context = context
        self._conversation = (
            Conversation.load(dump=conversation_dump) if conversation_dump is not None else Conversation()
        )
        if system_message is not None:
            self._conversation.set_system_message(message=system_message)

        self._get_tools_system_message_part = get_tools_system_message_part or _default_get_tools_system_message_part

    @property
    def conversation(self) -> Conversation:
        """Get the current conversation.
        
        Returns:
            The current Conversation instance.
        """
        return self._conversation

    @cached_property
    def tools_by_name(self) -> dict[str, Tool[ContextT, BaseModel, BaseModel]]:
        """Get a dictionary of tools indexed by name.
        
        Returns:
            Dictionary mapping tool names to Tool instances.
        """
        return {tool.name: tool for tool in self._tools}

    @contextmanager
    def tool_aware_conversation(self) -> Iterator[None]:
        """Context manager that temporarily adds tool information to the conversation's system message.
        
        Yields:
            None
        """
        message_part = self._get_tools_system_message_part(tools=self._tools)
        with self._conversation.with_temporary_system_message(message_part=message_part):
            yield

    async def step[M: LLMModelAlias](self, *, user_message: LLMUserMessage, model: M, router: LLMRouter[M]) -> StepResult:
        """Process a single step of conversation with the agent.
        
        This method processes a user message, generates an AI response, and optionally
        executes a tool call based on the AI's decision.
        
        Args:
            user_message: The user's message to process.
            model: The LLM model to use for generating responses.
            router: The router to use for routing requests to the LLM.
            
        Returns:
            A StepResult containing the assistant message and optional tool message.
            
        Raises:
            FrizzError: If a tool is not found, parameters are invalid, or tool execution fails.
        """
        with self.conversation.session():
            self._conversation.add_user_message(message=user_message)

            with self.tool_aware_conversation():
                agent_message = await llm_structured(
                    messages=self._conversation.render(),
                    response_model=AgentMessage,
                    router=router,
                )

            assistant_message = LLMAssistantMessage(
                parts=[LLMMessagePart(content=agent_message.structured_response.text)]
            )
            self._conversation.add_assistant_message(message=assistant_message)

            if agent_message.structured_response.chosen_tool_name is not None:
                chosen_tool = self.tools_by_name.get(agent_message.structured_response.chosen_tool_name)
                if chosen_tool is None:
                    raise FrizzError(f"Tool {agent_message.structured_response.chosen_tool_name} not found")

                try:
                    # Render messages and tools for the router
                    rendered_messages = []
                    for message in self._conversation.render():
                        if isinstance(message, LLMToolMessage):
                            invocation_message, response_message = message.render_call_and_response()
                            rendered_messages.append(invocation_message)
                            rendered_messages.append(response_message)
                        else:
                            rendered_messages.append(message.render())
                    
                    rendered_tools = [chosen_tool.as_llm_tool().render()]
                    
                    # Use the underlying _completion method directly to bypass the broken llm_tool_call
                    raw_response = router._completion(
                        model=model,
                        messages=rendered_messages,
                        tools=rendered_tools,
                        tool_choice="required",
                    )
                    
                    if len(raw_response.choices) == 0:
                        raise FrizzError("No response from model")
                    
                    tool_calls = raw_response.choices[0].message.tool_calls or []
                    if len(tool_calls) == 0:
                        raise FrizzError("Model did not make a tool call")
                    
                    tool_call = tool_calls[0]
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError as error:
                        raise FrizzError(f"Invalid tool arguments: {error}")
                    
                    parameters = chosen_tool.parameters_model.model_validate(arguments)
                except ValidationError as error:
                    raise FrizzError(
                        f"Invalid tool parameters for tool {agent_message.structured_response.chosen_tool_name}: {error}"
                    )
                except Exception as error:
                    raise FrizzError(f"Error calling tool: {error}")

                try:
                    result = await chosen_tool(
                        context=self._context, parameters=parameters, conversation=self._conversation
                    )
                except Exception as error:
                    raise FrizzError(
                        f"Error calling tool {agent_message.structured_response.chosen_tool_name}: {error}"
                    )

                tool_message = LLMToolMessage(
                    tool_call_id=tool_call.id,
                    name=tool_call.function.name,
                    response=result.model_dump(),
                    function_call=LLMToolMessageFunctionCall(
                        name=tool_call.function.name,
                        arguments=arguments,
                    ),
                )
                self._conversation.add_tool_message(tool_message=tool_message)
            else:
                tool_message = None

        return StepResult(assistant_message=assistant_message, tool_message=tool_message)


def _default_get_tools_system_message_part(*, tools: list[Tool[Any, Any, Any]]) -> LLMMessagePart:
    """Generate the default system message part describing available tools.
    
    This function creates a message part that instructs the LLM on how to use tools
    in conversation and provides information about the available tools.
    
    Args:
        tools: List of Tool instances available for use.
        
    Returns:
        A LLMMessagePart containing instructions and tool descriptions.
    """
    return LLMMessagePart(
        content=f"""
        Tools are available for use in this conversation.

        When using a tool, your message to the user should indicate to them that you are going to use that tool.
        Don't use the term "tool", since they don't know what that is. For example, if you have a tool to
        get the weather, you might say "let me check the weather".

        When calling a tool, do not include the tool name or any part of the call in the message to the user.
        Only include the tool name in the chosen tool field of the AgentMessage.

        You have access to the following tools:
        {"\n".join([yaml.safe_dump(tool.as_llm_tool().render()) for tool in tools])}
    """
    )
