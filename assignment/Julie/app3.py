import hashlib, json, time

# Simple Block class
class Block:
    def __init__(self, index, data, prev_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


# Build a small blockchain
blockchain = [Block(0, "Genesis Block", "0")]

# Add new blocks
for i in range(1, 4):
    data = f"Transaction Data #{i}"
    prev_hash = blockchain[-1].hash
    blockchain.append(Block(i, data, prev_hash))

# Print the chain
for block in blockchain:
    print(f"\nBlock {block.index}")
    print(f"Timestamp: {time.ctime(block.timestamp)}")
    print(f"Data: {block.data}")
    print(f"Prev Hash: {block.prev_hash[:10]}...")
    print(f"Hash: {block.hash[:10]}...")