import random

def bubble_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        is_sorted = True

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                is_sorted = False
                yield {j: arr[j], j + 1: arr[j + 1]}, (j, j + 1)

        if is_sorted:
            break

    yield {}, ()

def selection_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        minIndex = i
        for j in range(i + 1, n):
            if arr[minIndex] > arr[j]:
                minIndex = j
            
        if minIndex != i:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
            yield {i: arr[i], minIndex: arr[minIndex]}, (i, minIndex)

    yield {}, ()

def insertion_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            yield {j + 1: arr[j + 1]}, (j, j + 1)
            j -= 1

        if arr[j + 1] != key:
            arr[j + 1] = key
            yield {j + 1: arr[j + 1]}, (j + 1,)

    yield {}, ()

def merge_sort_steps(arr):
    arr = arr.copy()
    n = len(arr)

    def merge(left, mid, right):
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        i = 0
        j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                value = left_arr[i]
                i += 1
            else:
                value = right_arr[j]
                j += 1

            if arr[k] != value:
                arr[k] = value
                yield {k: value}, (k,)
            k += 1

        while i < len(left_arr):
            value = left_arr[i]
            i += 1
            if arr[k] != value:
                arr[k] = value
                yield {k: value}, (k,)
            k += 1

        while j < len(right_arr):
            value = right_arr[j]
            j += 1
            if arr[k] != value:
                arr[k] = value
                yield {k: value}, (k,)
            k += 1

    def divide(left, right):
        if left >= right:
            return

        mid = (left + right) // 2

        yield from divide(left, mid)
        yield from divide(mid + 1, right)
        yield from merge(left, mid, right)

    yield from divide(0, n - 1)
    yield {}, ()

def quick_sort_steps(arr):
    arr = arr.copy()
    n = len(arr)

    def divide(left, right):

        def median_of_three(left, right):
            mid = (left + right) // 2

            a = arr[left]
            b = arr[mid]
            c = arr[right]

            if (a <= b <= c) or (c <= b <= a):
                pivot_index = mid
            elif (b <= a <= c) or (c <= a <= b):
                pivot_index = left
            else:
                pivot_index = right

            return pivot_index

        pivot_index = median_of_three(left=left, right=right)
        if pivot_index != right:
            arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
            yield {
                pivot_index: arr[pivot_index],
                right: arr[right],
            }, (pivot_index, right)
        pivot = arr[right]

        i = left

        for j in range(left, right):
            if arr[j] <= pivot:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    yield {i: arr[i], j: arr[j]}, (i, j)
                i += 1

        # Put pivot in its correct position
        if i != right:
            arr[i], arr[right] = arr[right], arr[i]
            yield {i: arr[i], right: arr[right]}, (i, right)

        return i

    def quick_sort(left, right):
        if left < right:
            p = yield from divide(left, right)

            yield from quick_sort(left, p - 1)
            yield from quick_sort(p + 1, right)

    yield from quick_sort(0, n - 1)

    yield {}, ()

def heap_sort_steps(arr):  # O(n log n)
    arr = arr.copy()
    n = len(arr)

    def heapify(heap_size, i):
        largest = i
        left_child = i * 2 + 1
        right_child = i * 2 + 2

        if left_child < heap_size and arr[left_child] > arr[largest]:
            largest = left_child

        if right_child < heap_size and arr[right_child] > arr[largest]:
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield {i: arr[i], largest: arr[largest]}, (i, largest)
            yield from heapify(heap_size, largest)

    def heap_sort():
        # build Max Heap
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(n, i)

        # sort heap
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            yield {0: arr[0], i: arr[i]}, (0, i)

            yield from heapify(i, 0)

    yield from heap_sort()

    yield {}, ()

def counting_sort_steps(arr):
    if not arr:
        yield {}, ()
        return

    arr = arr.copy()

    min_num = min(arr)
    max_num = max(arr)
    counting_list = [0] * (max_num - min_num + 1)
    output = [0] * len(arr)

    for value in arr:
        counting_list[value - min_num] += 1

    for i in range(1, len(counting_list)):
        counting_list[i] += counting_list[i - 1]

    for value in reversed(arr):
        count_index = value - min_num
        output[counting_list[count_index] - 1] = value
        counting_list[count_index] -= 1

    for i, value in enumerate(output):
        arr[i] = value
        yield {i: value}, (i,)

    yield {}, ()

def shell_sort_steps(arr): # O(n^2)

    yield {}, ()

def tim_sort_steps(arr): # O(n^2)

    yield {}, ()

def radix_sort_steps(arr): # O(n^2)

    yield {}, ()



if __name__ == "__main__":
    print(arr)
    print(counting_sort_steps(arr))
