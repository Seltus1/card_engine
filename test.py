import timeit
def check_in_set():
    natural_ranks = ("QUEEN", "JACK", "KING", "TEN", "ACE")
    rank = "KING"
    return rank in natural_ranks

def check_in_list():
    natural_ranks = ["QUEEN", "JACK", "KING", "TEN", "ACE"]
    rank = "KING"
    return rank in natural_ranks

time_taken_set = timeit.timeit(check_in_set, number=1000)
time_taken_list = timeit.timeit(check_in_list, number=1000)

print(f"The time taken for the set function is {time_taken_set} after 1000 iters")
print("----------------")
print(f"The time taken for the LIST function is {time_taken_list} after 1000 iters")