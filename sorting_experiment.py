import time
import random
import sys
import csv

#ca sa nu opreasca executia pentru prea multe elemente Python
sys.setrecursionlimit(2000000)

#defineste element linked list, date si next pt node-uri
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

#ia o lista clasica, o parcurge si creaza noduri, return head
def array_to_ll(arr):
    if not arr: return None
    head = Node(arr[0])
    curr = head
    for v in arr[1:]:
        curr.next = Node(v)
        curr = curr.next
    return head

#merge pt linked list, sorteaza jumatati si imbina next-urile dupa.
def merge_ll(head):
    if not head or not head.next:
        return head

    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    l, r = merge_ll(head), merge_ll(mid)

    dummy = Node(0)
    curr = dummy
    while l and r:
        if l.data < r.data:
            curr.next, l = l, l.next
        else:
            curr.next, r = r, r.next
        curr = curr.next
    curr.next = l or r
    return dummy.next

#bubble pt array normal
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

#selection pt array normal
#cauta cel mai mic si il aduce in fata
def selection_sort(arr):
    for i in range(len(arr)):
        m = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[m]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]

#insertion pt array normal
#insereaza fiecare element nou in pozitia buna fata de alea sortate
def insertion_sort(arr):
    for i in range(1, len(arr)):
        k, j = arr[i], i - 1
        while j >= 0 and k < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = k

#merge pt array normal
#O(nlogn) imparte lista si dupa le recompune sortat. ft stabil
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L, R = arr[:mid], arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i];
                i += 1
            else:
                arr[k] = R[j];
                j += 1
            k += 1
        arr[k:] = L[i:] if i < len(L) else R[j:]

#quick pt array normal
#alege pivot aleatoriu, le separa,
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    p = arr[random.randint(0, len(arr) - 1)]
    return quick_sort([x for x in arr if x < p]) + \
        [x for x in arr if x == p] + \
        quick_sort([x for x in arr if x > p])

#generare liste
def get_data(n, case):

    if case == "Random": return [random.randint(0, 1000000) for _ in range(n)] # perform. medie
    if case == "Sorted": return list(range(n))
    if case == "Reverse": return list(range(n, 0, -1)) #cel mai rau pt bubble si selection
    if case == "Flat": return [random.randint(0, 5) for _ in range(n)] #bun pt eficienta pivoti in Quick Sort
    if case == "Almost":
        d = list(range(n))
        for _ in range(int(n * 0.02)):
            i, j = random.randint(0, n - 1), random.randint(0, n - 1)
            d[i], d[j] = d[j], d[i]
        return d
    return [] #evidentiaza eficienta insertion sort


def main():
    try:
        user_input = input("Enter N: ")
        n = int(user_input)
    except ValueError:
        return

    cases = ["Random", "Sorted", "Reverse", "Almost", "Flat"]
    algos = [
        ("Bubble", bubble_sort),
        ("Selection", selection_sort),
        ("Insertion", insertion_sort),
        ("Merge", merge_sort),
        ("Quick", quick_sort)
    ]# lista tuples, pot fi apelate in loop-uri pt ca in python sunt ca obiectele

    # Lista in care colectam datele pentru CSV
    results_list = []

    print(f"\nResults for N = {n}")
    print(f"{'Algorithm':<15} | {'Case':<10} | {'Time (ns)':<15}")
    print("-" * 50)

    for case in cases:
        data = get_data(n, case)
        for name, func in algos:
            if n > 100000 and name in ["Bubble", "Selection", "Insertion"]: #pt alg astia se sare daca e introdus o lista m mare de 100.000
                print(f"{name:<15} | {case:<10} | SKIPPED")
                results_list.append([name, case, "SKIPPED"])
                continue
            current_copy = list(data) #facem o copie a listei originale, fiecare alg primeste lista originala

            start_ns = time.perf_counter_ns() #cel mai precis in python, mai precis decat .time()
            if name == "Quick": #pt ca quick sort e out-of-place, foloseste list comprehension
                quick_sort(current_copy)
            else:
                func(current_copy) #pt restul alg care sunt in-place
            duration_ns = time.perf_counter_ns() - start_ns

            print(f"{name:<15} | {case:<10} | {duration_ns:,} ns")
            results_list.append([name, case, duration_ns])

        # Linked List Merge Sort Test
        start_ll_ns = time.perf_counter_ns()
        head = array_to_ll(data)
        merge_ll(head)
        duration_ll_ns = time.perf_counter_ns() - start_ll_ns
        print(f"{'Merge_LL':<15} | {case:<10} | {duration_ll_ns:,} ns")
        results_list.append(["Merge_LL", case, duration_ll_ns])
        print("-" * 50)

    #scrie in fisier csv
    filename = f"rezultate_{n}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Case", "Time (ns)"])
        writer.writerows(results_list)

    print(f"\n rezultatele in: {filename}")


if __name__ == "__main__":
    main()