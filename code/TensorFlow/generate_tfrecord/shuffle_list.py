import random

with open('image_list','r') as source:
    data = [ (random.random(), line) for line in source ]
    data.sort()
    with open('shuffle_image_list','w') as target:
        for _, line in data:
            target.write( line )
