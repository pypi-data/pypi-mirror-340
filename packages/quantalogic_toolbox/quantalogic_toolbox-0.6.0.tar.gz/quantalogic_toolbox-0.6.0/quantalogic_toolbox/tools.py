from typing import Callable


def tool(func: Callable) -> Callable:
    """
    A decorator to mark a callable as a tool for exposure to quantalogic.

    Args:
        func: The function to be marked as a tool.

    Returns:
        Callable: The original function with an _is_tool attribute set to True.
    """
    func._is_tool = True
    return func


if __name__ == "__main__":
    from typing import List

    @tool
    def calculate_average(numbers: List[float], precision: int = 2) -> float:
        """
        Calculate the average of a list of numbers with specified precision.

        Args:
            numbers: List of numbers to average.
            precision: Number of decimal places for the result.

        Returns:
            float: The average value rounded to specified precision.

        Examples:
            >>> calculate_average([1.0, 2.0, 3.0])
            2.0
            >>> calculate_average([1.234, 5.678, 9.012], 1)
            5.3

        Notes:
            - Returns 0.0 if the input list is empty.
        """
        if not numbers:
            return 0.0
        return round(sum(numbers) / len(numbers), precision)

    # Access and print metadata for demonstration
    print("Tool Example:")
    print(f"Function marked as tool: {hasattr(calculate_average, '_is_tool') and calculate_average._is_tool}")
    print(f"Name: {calculate_average.__name__}")
    print(f"Docstring: {calculate_average.__doc__.strip().splitlines()[0]}")