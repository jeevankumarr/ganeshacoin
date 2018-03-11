
import hashlib
import time


def proof_of_work(trailing_zero_count=1):
    x = 5
    y = 0
    #print(trailing_zero_count)

    expected_value = "0"*trailing_zero_count

    while hashlib.sha256(f'{x*y}'.encode()).hexdigest()[-trailing_zero_count:] != expected_value:
        # print(hashlib.sha256(f'{x*y}'.encode()).hexdigest()[-2:])
        y += 1

    #print(f'the solution is y = {y}')
    return y

def profile_proof_of_work():
    for v in range(1,8):
        start = time.time()


        y = proof_of_work(trailing_zero_count=v)
        print(v, y, round(time.time() - start, 5))
    """
    1 21 6e-05
    2 254 0.00037
    3 4043 0.00595
    4 22474 0.0359
    5 840258 1.34215
    6 5199280 8.53344
    7 73102419 117.54263
    """
if __name__ == "__main__":
    profile_proof_of_work()