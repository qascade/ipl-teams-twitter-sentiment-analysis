import json

a = ['pbks.json', 'csk.json', 'mi.json', 'rcb.json', 'gt.json', 'lsg.json', 'srh.json', 'rr.json']
for file in a: 
    with open(file) as f:
        data = json.load(f)

    new_data = []
    for tweet in data:
        if "\n" in tweet["text"]:
            tweet["text"] = tweet["text"].replace("\n", " ")
            new_data.append({"text": tweet["text"]})

    with open(file, 'w') as f:
        json.dump(new_data, f, separators=(',', ':'), ensure_ascii=False)