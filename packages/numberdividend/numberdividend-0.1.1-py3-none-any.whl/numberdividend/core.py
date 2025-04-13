from typing import List, Tuple
import matplotlib.pyplot as plt
from numberdividend import controller

class NumberCore:
    def dividend(array: List[float], target_sum: float, limit: int = None) -> List[Tuple[int, int]]:
        """
        Calculate the dividend distribution of an array.
        :param array: List of float numbers to be distributed.
        :param target_sum: Target sum for the distribution.
        :param limit: Optional limit on the number of elements to consider from the array.
        :return: List of tuples containing the index and the dividend value.
        """
        controller.check_type_list(array)
        controller.check_type_float(target_sum)
        if limit is not None:
            controller.check_type_int(limit)

        if limit:
            array = array[:limit]

        total = sum(array)
        if total == 0:
            raise ValueError("The sum of the array elements is zero, cannot calculate dividend.")
        
        scale = target_sum / total
        dividend = [round(x * scale, 2) for x in array]
        return dividend
    
    def display(array: List[float]):

        """
        Display the dividend distribution using matplotlib.
        :param array: List of dividend values to be displayed.
        :return: None
        """

        print(f"Dividend Distribution Sum: {sum(array)}")
        
        fig, ax = plt.subplots()
        ax.bar(range(len(array)), array, color='orange')
        
        plt.title('Dividend Distribution')
        plt.xlabel('Index')
        plt.ylabel('Dividend Value')
        plt.grid(True)
        plt.show()
    