import math

pairs = [
    ('thread-1', 1, 4000), ('thread_2', 4001, 8000),
    ('thread-3', 8001, 12000), ('thread_4', 12001, 16000),
    ('thread-5', 16001, 20000), ('thread_6', 20001, 24000),
    ('thread-7', 24001, 28000), ('thread_8', 28001, 32000),
    ('thread-9', 32001, 36000), ('thread_10', 36001, 40000),
    ('thread-11', 40001, 44000), ('thread_12', 44001, 48000),
    ('thread-13', 48001, 52000), ('thread_14', 52001, 56000),
    ('thread-15', 56001, 60000), ('thread_16', 60001, 64000),
    ('thread-17', 68001, 72000), ('thread_18', 72001, 76000),
    ('thread-19', 76001, 80000),
]


def get_pairs(max_id, threads):
    data = []
    counter = 1
    l_ids = [x for x in range(1, max_id + 1)]
    chunk_size = math.floor(max_id / threads)
    chunks = [l_ids[i:i + chunk_size] for i in range(0, len(l_ids), chunk_size)]
    for chunk in chunks:
        data.append((f'thread-{counter}', chunk[0], chunk[-1]))
        counter += 1
    print(data)
    return data


get_pairs(max_id=80000, threads=40)
