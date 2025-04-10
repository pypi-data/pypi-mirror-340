from fnet_shell_flow.lib import default
import argparse
def main():
    # Create an argument parser to handle command-line input
    parser = argparse.ArgumentParser(description="fnet_shell_flow")
    
    # Parse known and unknown arguments. We only need unknown arguments here.
    _, unknown_args = parser.parse_known_args()
    
    # Convert unknown arguments into a kwargs dictionary
    kwargs = {}
    for i in range(0, len(unknown_args), 2):
        key = unknown_args[i].lstrip("--")  # Remove the leading "--" from the argument name
        value = unknown_args[i + 1] if i + 1 < len(unknown_args) else None  # Handle key-value pairs
        kwargs[key] = value  # Add the key-value pair to the kwargs dictionary

    # Pass the kwargs to the default function
    result=default(**kwargs)
    
    print(result)  # Print the result as a string

# Entry point for the script
if __name__ == "__main__":
    main()