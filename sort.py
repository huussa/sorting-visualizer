import random

def bubble_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        is_sorted = True

        for j in range(n - i - 1):
            yield arr.copy(), (j, j + 1)

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                is_sorted = False
                yield arr.copy(), (j, j + 1)

        if is_sorted:
            break

    yield arr.copy(), ()

def selection_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        minIndex = i
        for j in range(i + 1, n):
            yield arr.copy(), (minIndex, j)

            if arr[minIndex] > arr[j]:
                minIndex = j
            
        if minIndex != i:
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
            yield arr.copy(), (i, minIndex)

    yield arr.copy(), ()

def insertion_sort_steps(arr): # O(n^2)
    arr = arr.copy()
    n = len(arr)

    for i in range(1, n):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            yield arr.copy(), (j + 1, j)
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key
        yield arr.copy(), (j + 1, j + 1)

    yield arr.copy(), ()

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
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1

            yield arr.copy(), (k,)
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            yield arr.copy(), (k,)
            k += 1

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            yield arr.copy(), (k,)
            k += 1

    def divide(left, right):
        if left >= right:
            return

        mid = (left + right) // 2

        yield from divide(left, mid)
        yield from divide(mid + 1, right)
        yield from merge(left, mid, right)

    yield from divide(0, n - 1)
    yield arr.copy(), ()

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
        arr[pivot_index], arr[right] = arr[right], arr[pivot_index]
        pivot = arr[right]

        i = left

        for j in range(left, right):
            # Highlight the current element and pivot
            yield arr.copy(), (j, right)

            if arr[j] <= pivot:
                arr[i], arr[j] = arr[j], arr[i]

                # Show the swap
                yield arr.copy(), (i, j)
                i += 1

        # Put pivot in its correct position
        arr[i], arr[right] = arr[right], arr[i]
        yield arr.copy(), (i, right)

        return i

    def quick_sort(left, right):
        if left < right:
            p = yield from divide(left, right)

            yield from quick_sort(left, p - 1)
            yield from quick_sort(p + 1, right)

    yield from quick_sort(0, n - 1)

    yield arr.copy(), ()

def heap_sort_steps(arr): # O(n^2)

    yield arr.copy(), ()

def counting_sort_steps(arr): # O(n^2)

    yield arr.copy(), ()

def shell_sort_steps(arr): # O(n^2)

    yield arr.copy(), ()

def tim_sort_steps(arr): # O(n^2)

    yield arr.copy(), ()

def radix_sort_steps(arr): # O(n^2)

    yield arr.copy(), ()

arr = [8, 3, 6, 2, 7, 1, 5, 4]

if __name__ == "__main__":
    arr = list(range(1, 1001))
    random.shuffle(arr)
    left = 0
    right = len(arr) - 1

    print(arr)
