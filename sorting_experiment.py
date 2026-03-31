import time
import random
import sys
import csv
import string

# ca sa nu opreasca executia pentru prea multe elemente Python
sys.setrecursionlimit(2000000)

# defineste element linked list, date si next pt node-uri
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# ia o lista clasica, o parcurge si creaza noduri, return head
def array_to_ll(arr):
    if not arr: return None
    head = Node(arr[0])
    curr = head
    for v in arr[1:]:
        curr.next = Node(v)
        curr = curr.next
    return head


# merge pt linked list, sorteaza jumatati si imbina next-urile dupa.
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


# bubble pt array normal
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# selection pt array normal
# cauta cel mai mic si il aduce in fata
def selection_sort(arr):
    for i in range(len(arr)):
        m = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[m]:
                m = j
        arr[i], arr[m] = arr[m], arr[i]


# insertion pt array normal
# insereaza fiecare element nou in pozitia buna fata de alea sortate
def insertion_sort(arr):
    for i in range(1, len(arr)):
        k, j = arr[i], i - 1
        while j >= 0 and k < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = k


# merge pt array normal
# O(nlogn) imparte lista si dupa le recompune sortat. ft stabil
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


# quick pt array normal
# alege pivot aleatoriu, le separa,
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    p = arr[random.randint(0, len(arr) - 1)]
    return quick_sort([x for x in arr if x < p]) + \
        [x for x in arr if x == p] + \
        quick_sort([x for x in arr if x > p])


# generare liste - Modificată pentru a suporta tipuri de date
def get_data(n, case, data_type):
    # Generăm baza de date în funcție de tip
    if data_type == "int":
        raw_data = [random.randint(0, 1000000) for _ in range(n)]
    elif data_type == "float":
        raw_data = [random.uniform(0.0, 1000000.0) for _ in range(n)]
    elif data_type == "string":
        # Generează cuvinte aleatorii de 5 litere
        raw_data = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(n)]

    if case == "Random":
        return raw_data
    if case == "Sorted":
        return sorted(raw_data)
    if case == "Reverse":
        return sorted(raw_data, reverse=True)
    if case == "Flat":
        # Luăm doar primele 5 elemente unice pentru a simula distribuția plată
        subset = raw_data[:5]
        return [random.choice(subset) for _ in range(n)]
    if case == "Almost":
        d = sorted(raw_data)
        for _ in range(int(n * 0.02)):
            i, j = random.randint(0, n - 1), random.randint(0, n - 1)
            d[i], d[j] = d[j], d[i]
        return d
    return []


def main():
    try:
        user_input = input("Enter N: ")
        n = int(user_input)
    except ValueError:
        return

    # Am adăugat tipurile de date aici
    data_types = ["int", "float", "string"]
    cases = ["Random", "Sorted", "Reverse", "Almost", "Flat"]
    algos = [
        ("Bubble", bubble_sort),
        ("Selection", selection_sort),
        ("Insertion", insertion_sort),
        ("Merge", merge_sort),
        ("Quick", quick_sort)
    ]

    results_list = []

    print(f"\nResults for N = {n}")
    print(f"{'Algorithm':<15} | {'Type':<8} | {'Case':<10} | {'Time (ns)':<15}")
    print("-" * 65)

    for dtype in data_types:
        for case in cases:
            data = get_data(n, case, dtype)
            for name, func in algos:
                if n > 10000 and name in ["Bubble", "Selection", "Insertion"]:
                    print(f"{name:<15} | {dtype:<8} | {case:<10} | SKIPPED")
                    results_list.append([name, dtype, case, "SKIPPED"])
                    continue

                current_copy = list(data)

                start_ns = time.perf_counter_ns()
                if name == "Quick":
                    quick_sort(current_copy)
                else:
                    func(current_copy)
                duration_ns = time.perf_counter_ns() - start_ns

                print(f"{name:<15} | {dtype:<8} | {case:<10} | {duration_ns:,} ns")
                results_list.append([name, dtype, case, duration_ns])

            # test linked list, merge
            start_ll_ns = time.perf_counter_ns()
            head = array_to_ll(data)
            merge_ll(head)
            duration_ll_ns = time.perf_counter_ns() - start_ll_ns
            print(f"{'Merge_LL':<15} | {dtype:<8} | {case:<10} | {duration_ll_ns:,} ns")
            results_list.append(["Merge_LL", dtype, case, duration_ll_ns])
            print("-" * 65)

    # scrie in fisier csv
    filename = f"rezultate_{n}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Data Type", "Case", "Time (ns)"])
        writer.writerows(results_list)

    print(f"\n rezultatele in: {filename}")


if __name__ == "__main__":
    main()