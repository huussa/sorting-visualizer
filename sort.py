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

def merge_sort_steps(arr): # O(n log n)
    arr = arr.copy()
    n = len(arr)

    def merge(left, right):
        result = []
        i = 0
        j = 0

    if n <= 1:
        return arr
    
    mid = n // 2
    left = merge_sort_steps(arr[:mid])
    right = merge_sort_steps(arr[mid:])

    return merge(left, right)

    yield arr.copy(), ()

def quick_sort_steps(arr): # O(n log n)

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
    # arr = list(range(100))

    # shuffled_arr = arr
    # random.shuffle(shuffled_arr)

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    print(left, right)