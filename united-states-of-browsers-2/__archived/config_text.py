- type: local
          - product: firefox
          locations:
            - os: nt
              dirpaths:
                - C:\\Users\\kshit_7khjmc8\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles
                - os: linux
                  dirpaths: null
                - os: macos
                  dirpaths: null
          profiles:
            - default
            - default-release
          datasources:
            - collection: moz_places
              file: places.sqlite
              type: sqlite
              info: history
              fields:
                - id
                - url
                - title
                - visit_count
                - last_visit_date
