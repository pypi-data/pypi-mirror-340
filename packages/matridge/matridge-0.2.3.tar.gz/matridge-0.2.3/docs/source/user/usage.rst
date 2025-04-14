Usage
=====

Be patient
----------

Matrix the protocol, Python the language, and slidge the implementation are all **slow**.
Just wait, it takes time to log in, join rooms and send messages: this is all expected.

Everything is a MUC
-------------------

Standard XMPP direct messages are not supported.
Direct channels rooms (1:1 messages) are group chats of 2 participants.

E2EE
----

End-to-end encryption is not possible, but you can use end-to-bridge encryption.
First, verify your slidge session using another client using the emoji verification workflow.

Then you will have to either "verify", "ignore", or "blacklist" the keys
corresponding to your rooms and your other sessions.
This can be done using the adhoc or chat command "verify" (send "verify" to
the JID of matridge, eg ``matridge.example.com``).
If you don't really care about all this, you can use the shortcut "verify all".
