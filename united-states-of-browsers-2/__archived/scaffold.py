from typing import Collection


class Scaffold:
    def __init__(
        self,
        configurations: Collection[Configuration],
        data_sources: Collection[DataSource],
        data_processors: Collection[DataProcessors],
        data_merger: DataMerger,
        data_indexer: DataIndexer,

        ):
