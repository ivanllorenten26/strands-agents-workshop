
def terminal_loop(agent):
    """
    Run an interactive terminal loop for the agent.

    Args:
        agent: Initialized Strands agent instance
    """

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nAgent: Goodbye! Thanks for chatting!")
                break

            # Skip empty inputs
            if not user_input:
                continue

            # Process the query with the agent
            response = agent(user_input)

            # Display the response
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user...")
            break
        except Exception as e:
            print(f"\nError processing request: {e}\n")
            continue
