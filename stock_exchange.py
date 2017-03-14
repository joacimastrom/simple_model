import csv
from intervaltree import IntervalTree
from datetime import datetime

def parse_date(dt):
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

def create_interval_tree(filename):
    tree = IntervalTree()

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        row = next(reader)
        state = "initial"
        state_agg_id = row[0]
        state_id = None
        state_date = None
        i = 0

        while row != None:
            i += 1
            if state == "initial":
                if row[3] == 'instock':
                    # print("%s - Start interval for %s" % (i, row[1]))
                    state_id = row[1]
                    state_date = parse_date(row[2])
                    state = "begin"
                else:
                    # print("%s - noop" % i)
                    state = "initial"
            elif state == "begin":
                if row[0] == state_agg_id:
                    if row[3] == 'instock':
                        print(
                            "This should not happen, instock followed by another instock for the same aggregate_id")
                        break
                    else:
                        # print("%s - End interval for %s" % (i, row[1]))
                        tree[state_date:parse_date(row[2])] = int(state_id)
                        state = "initial"
                else:
                    tree[state_date:datetime.now()] = int(state_id)
                    if row[3] == 'instock':
                        # print(
                        #    "%s - End previous interval(%s) and start new interval for %s" % (i, state_id, row[1]))
                        state_id = row[1]
                        state_date = parse_date(row[2])
                        state = "begin"
                    else:
                        # print("%s - End previous interval(%s)" % (i, state_id))
                        state = "initial"

            state_agg_id = row[0]
            row = next(reader, None)

    return tree

if __name__ == "__main__":
    tree = create_interval_tree('sql/stock_exchange.csv')

    # The total count of products on the market can be ploted
    print(len(set(map((lambda x: x.data), tree[parse_date("2016-12-31 15:00:00")]))))
    print(len(set(map((lambda x: x.data), tree[parse_date("2017-01-01 15:00:00")]))))
    print(len(set(map((lambda x: x.data), tree[parse_date("2017-01-02 15:00:00")]))))
    print(len(set(map((lambda x: x.data), tree[parse_date("2017-01-03 15:00:00")]))))
    print(len(set(map((lambda x: x.data), tree[parse_date("2017-01-04 15:00:00")]))))
