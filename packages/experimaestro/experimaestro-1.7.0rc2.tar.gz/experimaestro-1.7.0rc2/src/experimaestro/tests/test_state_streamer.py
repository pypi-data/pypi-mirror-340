from .state_streamer_pb2 import PartialUpdate, GlobalState

# Writing
with open("log.bin", "wb") as f:
    writer = StreamingStateWriter(f, PartialUpdate, GlobalState)
    for i in range(1000):
        writer.write_partial(PartialUpdate(updated_field=i))
        if i % 100 == 0:
            writer.write_snapshot_if_needed(GlobalState(field=i))

# Reading
with open("log.bin", "rb") as f:
    reader = StreamingStateReader(f, PartialUpdate, GlobalState)
    last_snapshot = reader.seek_last_snapshot()
    print("Last Snapshot:", last_snapshot)

    for msg in reader:
        print(type(msg).__name__, msg)
