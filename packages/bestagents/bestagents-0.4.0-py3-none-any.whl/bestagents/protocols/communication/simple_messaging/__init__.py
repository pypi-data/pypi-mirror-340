"""
Simple Messaging Protocol for BestAgents.

This protocol enables direct and broadcast messaging between agents with support for text and file attachments.
Key features:
- Direct messaging between agents
- Broadcast messaging to all agents
- File transfer capabilities
- Support for text and binary file attachments
"""

from bestagents.protocols.communication.simple_messaging.adapter import SimpleMessagingAgentClient
from bestagents.protocols.communication.simple_messaging.protocol import SimpleMessagingNetworkProtocol

__all__ = ["SimpleMessagingAgentClient", "SimpleMessagingNetworkProtocol"] 