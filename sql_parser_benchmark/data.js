window.BENCHMARK_DATA = {
  "lastUpdate": 1722450183460,
  "repoUrl": "https://github.com/amsdal/amsdal-glue",
  "entries": {
    "SQL Parser Benchmark": [
      {
        "commit": {
          "author": {
            "email": "127112856+oleksii-kuzmenko-litslink@users.noreply.github.com",
            "name": "Oleksii Kuzmenko",
            "username": "oleksii-kuzmenko-litslink"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "3419d844b2ba7e855d5be9e8b58c7be28546d85b",
          "message": "Merge pull request #43 from amsdal/feature/benchmarks\n\nFix benchmark output file path",
          "timestamp": "2024-07-23T18:20:13+03:00",
          "tree_id": "b1f9f7457a2326d906c8caeb6885159c805f99b3",
          "url": "https://github.com/amsdal/amsdal-glue/commit/3419d844b2ba7e855d5be9e8b58c7be28546d85b"
        },
        "date": 1721748072167,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 27976.18675352321,
            "unit": "iter/sec",
            "range": "stddev: 0.00016452763955812147",
            "extra": "mean: 35.7446856074502 usec\nrounds: 3559"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 26731.952150993977,
            "unit": "iter/sec",
            "range": "stddev: 0.00011389414153182107",
            "extra": "mean: 37.40841650290089 usec\nrounds: 12734"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 40055.175388463766,
            "unit": "iter/sec",
            "range": "stddev: 0.00007820459049297067",
            "extra": "mean: 24.965562884241137 usec\nrounds: 15327"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 23341.34122546834,
            "unit": "iter/sec",
            "range": "stddev: 0.000072105307634237",
            "extra": "mean: 42.84243952994758 usec\nrounds: 9251"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 72846.85127033069,
            "unit": "iter/sec",
            "range": "stddev: 0.00007579568896934477",
            "extra": "mean: 13.727429292572367 usec\nrounds: 26718"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 24990.32638843802,
            "unit": "iter/sec",
            "range": "stddev: 0.00011922528135219534",
            "extra": "mean: 40.01548376985817 usec\nrounds: 10179"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 40958.969708752,
            "unit": "iter/sec",
            "range": "stddev: 0.00009298690842276822",
            "extra": "mean: 24.41467661688577 usec\nrounds: 10050"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 30003.363048598043,
            "unit": "iter/sec",
            "range": "stddev: 0.000026875400574019948",
            "extra": "mean: 33.329597031514325 usec\nrounds: 10568"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 9428.975449795007,
            "unit": "iter/sec",
            "range": "stddev: 0.00017915946344971475",
            "extra": "mean: 106.05606148033195 usec\nrounds: 4737"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 17323.38386280032,
            "unit": "iter/sec",
            "range": "stddev: 0.00007263457240095175",
            "extra": "mean: 57.72544255325127 usec\nrounds: 8770"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 10620.508586737562,
            "unit": "iter/sec",
            "range": "stddev: 0.00011310000216303911",
            "extra": "mean: 94.15744941336965 usec\nrounds: 3502"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 7698.164414296789,
            "unit": "iter/sec",
            "range": "stddev: 0.00019395712059772286",
            "extra": "mean: 129.90109670077084 usec\nrounds: 5322"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 6185.034836580653,
            "unit": "iter/sec",
            "range": "stddev: 0.0002489807510321785",
            "extra": "mean: 161.68057681512462 usec\nrounds: 3045"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 38156.24630662139,
            "unit": "iter/sec",
            "range": "stddev: 0.000019397919302893508",
            "extra": "mean: 26.20802874486284 usec\nrounds: 14610"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 30250.63404950371,
            "unit": "iter/sec",
            "range": "stddev: 0.00008500520248992293",
            "extra": "mean: 33.05715835124473 usec\nrounds: 13997"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 13129.966453999032,
            "unit": "iter/sec",
            "range": "stddev: 0.00009995997457429385",
            "extra": "mean: 76.16165688644445 usec\nrounds: 7503"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 4628.154010508565,
            "unit": "iter/sec",
            "range": "stddev: 0.0004033701364808337",
            "extra": "mean: 216.068868436406 usec\nrounds: 1592"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 7449.675299589487,
            "unit": "iter/sec",
            "range": "stddev: 0.00020923843730516508",
            "extra": "mean: 134.2340383687736 usec\nrounds: 3289"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 9964.096038595584,
            "unit": "iter/sec",
            "range": "stddev: 0.00016534639356659213",
            "extra": "mean: 100.36033335352595 usec\nrounds: 4989"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 22738.90459122641,
            "unit": "iter/sec",
            "range": "stddev: 0.0002458187957562962",
            "extra": "mean: 43.977492230907224 usec\nrounds: 7378"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 17998.010807281917,
            "unit": "iter/sec",
            "range": "stddev: 0.0001993521577600768",
            "extra": "mean: 55.56169571780702 usec\nrounds: 5141"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 15755.116606469152,
            "unit": "iter/sec",
            "range": "stddev: 0.00022829224795120186",
            "extra": "mean: 63.471443911077984 usec\nrounds: 8092"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 6863.3649141890055,
            "unit": "iter/sec",
            "range": "stddev: 0.0004868937299910423",
            "extra": "mean: 145.7011265614984 usec\nrounds: 3799"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 6942.986671381746,
            "unit": "iter/sec",
            "range": "stddev: 0.0003533947179693307",
            "extra": "mean: 144.03023472908188 usec\nrounds: 4425"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 39114.85847365709,
            "unit": "iter/sec",
            "range": "stddev: 0.0001925241325267574",
            "extra": "mean: 25.565732282362106 usec\nrounds: 9405"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 52326.74691760029,
            "unit": "iter/sec",
            "range": "stddev: 0.000019753015916848177",
            "extra": "mean: 19.110685431576986 usec\nrounds: 8002"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 63970.12410338933,
            "unit": "iter/sec",
            "range": "stddev: 0.00006893124455220534",
            "extra": "mean: 15.632297326542421 usec\nrounds: 16197"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 85987.18541044874,
            "unit": "iter/sec",
            "range": "stddev: 0.00007180846123029782",
            "extra": "mean: 11.62963987280929 usec\nrounds: 27101"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 79892.99969207175,
            "unit": "iter/sec",
            "range": "stddev: 0.000018561277278170172",
            "extra": "mean: 12.516741189519207 usec\nrounds: 25764"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 90171.5258686849,
            "unit": "iter/sec",
            "range": "stddev: 0.00002371275892622181",
            "extra": "mean: 11.089975359364344 usec\nrounds: 17059"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 127227.26858907304,
            "unit": "iter/sec",
            "range": "stddev: 0.000015900880211147405",
            "extra": "mean: 7.859950237789554 usec\nrounds: 28789"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 57285.39982868678,
            "unit": "iter/sec",
            "range": "stddev: 0.00004777942998121016",
            "extra": "mean: 17.45645492552241 usec\nrounds: 16383"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 79897.61424947123,
            "unit": "iter/sec",
            "range": "stddev: 0.000025633938050282992",
            "extra": "mean: 12.516018274057766 usec\nrounds: 26327"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 37549.74184097718,
            "unit": "iter/sec",
            "range": "stddev: 0.00009845467800298079",
            "extra": "mean: 26.631341547832502 usec\nrounds: 12162"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 24308.98008660317,
            "unit": "iter/sec",
            "range": "stddev: 0.000012480038813112015",
            "extra": "mean: 41.137061136970786 usec\nrounds: 304"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 174480.61386460796,
            "unit": "iter/sec",
            "range": "stddev: 0.00003711608761845958",
            "extra": "mean: 5.731295745990278 usec\nrounds: 11888"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 173240.64701505532,
            "unit": "iter/sec",
            "range": "stddev: 0.000002762328014629247",
            "extra": "mean: 5.772317393348779 usec\nrounds: 32253"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 201384.62270073884,
            "unit": "iter/sec",
            "range": "stddev: 0.000002417045920827532",
            "extra": "mean: 4.965622432284802 usec\nrounds: 38693"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 133070.35860432452,
            "unit": "iter/sec",
            "range": "stddev: 0.000016848959219699918",
            "extra": "mean: 7.5148215612271 usec\nrounds: 27880"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 153575.92089057047,
            "unit": "iter/sec",
            "range": "stddev: 0.0000538952782418837",
            "extra": "mean: 6.511437432385923 usec\nrounds: 49547"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "114298238+ams-amsdal@users.noreply.github.com",
            "name": "ams-amsdal",
            "username": "ams-amsdal"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bf719132f57962f32afa5c1ebd4c044c71b24706",
          "message": "Merge pull request #44 from amsdal/feature/google-site-verification\n\nAdded google site verification file",
          "timestamp": "2024-07-25T08:28:02-04:00",
          "tree_id": "73352afe7582621f3903ae38cff35253eef1aa36",
          "url": "https://github.com/amsdal/amsdal-glue/commit/bf719132f57962f32afa5c1ebd4c044c71b24706"
        },
        "date": 1721910587649,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 37968.62262033921,
            "unit": "iter/sec",
            "range": "stddev: 0.00004902459303189896",
            "extra": "mean: 26.337536918295147 usec\nrounds: 4377"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 28534.428072992025,
            "unit": "iter/sec",
            "range": "stddev: 0.00008410371153014041",
            "extra": "mean: 35.04538438415399 usec\nrounds: 14410"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 43217.1356160228,
            "unit": "iter/sec",
            "range": "stddev: 0.00005650008429843446",
            "extra": "mean: 23.138969895757015 usec\nrounds: 15349"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 24963.47329793851,
            "unit": "iter/sec",
            "range": "stddev: 0.000050550091948068275",
            "extra": "mean: 40.05852823703744 usec\nrounds: 9097"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 70798.53725262632,
            "unit": "iter/sec",
            "range": "stddev: 0.000057323534757065005",
            "extra": "mean: 14.12458560311434 usec\nrounds: 12872"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 20167.828093277443,
            "unit": "iter/sec",
            "range": "stddev: 0.0002161975119909073",
            "extra": "mean: 49.583921251953285 usec\nrounds: 6718"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 32942.170690287465,
            "unit": "iter/sec",
            "range": "stddev: 0.0000920400506870305",
            "extra": "mean: 30.356226655544468 usec\nrounds: 9783"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 26737.74831722461,
            "unit": "iter/sec",
            "range": "stddev: 0.00003300652815863248",
            "extra": "mean: 37.40030716632164 usec\nrounds: 10880"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 7205.011769482864,
            "unit": "iter/sec",
            "range": "stddev: 0.00023629582708540215",
            "extra": "mean: 138.79227848530977 usec\nrounds: 4885"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 14048.239529321936,
            "unit": "iter/sec",
            "range": "stddev: 0.0001005816491883017",
            "extra": "mean: 71.18329652002075 usec\nrounds: 9305"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 8710.493929220573,
            "unit": "iter/sec",
            "range": "stddev: 0.000152604580826001",
            "extra": "mean: 114.80405223007618 usec\nrounds: 6710"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6246.58447304948,
            "unit": "iter/sec",
            "range": "stddev: 0.00015102757071877926",
            "extra": "mean: 160.0874852992769 usec\nrounds: 2814"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4373.9567220463505,
            "unit": "iter/sec",
            "range": "stddev: 0.00031963660917021545",
            "extra": "mean: 228.6259475224417 usec\nrounds: 4448"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 25895.54003155334,
            "unit": "iter/sec",
            "range": "stddev: 0.00010063103108595653",
            "extra": "mean: 38.61668838655284 usec\nrounds: 13343"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 25290.789283734295,
            "unit": "iter/sec",
            "range": "stddev: 0.0000837663597867557",
            "extra": "mean: 39.54008666084405 usec\nrounds: 14978"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 10872.050942307744,
            "unit": "iter/sec",
            "range": "stddev: 0.0002823710350802145",
            "extra": "mean: 91.9789656345867 usec\nrounds: 5592"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6172.313292491339,
            "unit": "iter/sec",
            "range": "stddev: 0.0002649419668168757",
            "extra": "mean: 162.01381112920933 usec\nrounds: 4729"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 7625.65326990483,
            "unit": "iter/sec",
            "range": "stddev: 0.00025823245069312215",
            "extra": "mean: 131.13630591448072 usec\nrounds: 5137"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 7958.416170817729,
            "unit": "iter/sec",
            "range": "stddev: 0.00024615952462473994",
            "extra": "mean: 125.65314235096729 usec\nrounds: 4320"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 27476.84757106315,
            "unit": "iter/sec",
            "range": "stddev: 0.00007012705132590409",
            "extra": "mean: 36.394276942204094 usec\nrounds: 14527"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 14418.661663790557,
            "unit": "iter/sec",
            "range": "stddev: 0.0001636906960699586",
            "extra": "mean: 69.35456447468285 usec\nrounds: 1716"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 18196.329436078347,
            "unit": "iter/sec",
            "range": "stddev: 0.00011844754063010974",
            "extra": "mean: 54.95613846258868 usec\nrounds: 11326"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 9292.852007715408,
            "unit": "iter/sec",
            "range": "stddev: 0.0002307424433276599",
            "extra": "mean: 107.60959059390467 usec\nrounds: 5820"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 9142.562949578489,
            "unit": "iter/sec",
            "range": "stddev: 0.00016372143084638732",
            "extra": "mean: 109.37851951526395 usec\nrounds: 7509"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 52577.34904910642,
            "unit": "iter/sec",
            "range": "stddev: 0.00004702102039396414",
            "extra": "mean: 19.01959718558681 usec\nrounds: 4656"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 38012.161923890395,
            "unit": "iter/sec",
            "range": "stddev: 0.00014052888267963797",
            "extra": "mean: 26.307369783445715 usec\nrounds: 21860"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 53863.43759669178,
            "unit": "iter/sec",
            "range": "stddev: 0.0000801289065306084",
            "extra": "mean: 18.565469353954096 usec\nrounds: 15924"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 59673.132368104605,
            "unit": "iter/sec",
            "range": "stddev: 0.000083192833746113",
            "extra": "mean: 16.75796058151125 usec\nrounds: 26799"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 49653.30112269592,
            "unit": "iter/sec",
            "range": "stddev: 0.00012901435051457285",
            "extra": "mean: 20.139647866089454 usec\nrounds: 26982"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 55023.198243819075,
            "unit": "iter/sec",
            "range": "stddev: 0.00010469536049948523",
            "extra": "mean: 18.174152574134183 usec\nrounds: 14258"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 93446.4692121171,
            "unit": "iter/sec",
            "range": "stddev: 0.0000726830210887319",
            "extra": "mean: 10.701313901224758 usec\nrounds: 31610"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 55528.50050071748,
            "unit": "iter/sec",
            "range": "stddev: 0.00002727088745968371",
            "extra": "mean: 18.008770108731444 usec\nrounds: 15561"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 59323.78366644468,
            "unit": "iter/sec",
            "range": "stddev: 0.00010310720113701713",
            "extra": "mean: 16.85664565198039 usec\nrounds: 29039"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 32674.60277222907,
            "unit": "iter/sec",
            "range": "stddev: 0.00005970565713488385",
            "extra": "mean: 30.60480970406545 usec\nrounds: 10687"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 7925.727389631917,
            "unit": "iter/sec",
            "range": "stddev: 0.0005625254472072024",
            "extra": "mean: 126.17138476250842 usec\nrounds: 313"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 118150.68450738347,
            "unit": "iter/sec",
            "range": "stddev: 0.0001018176044786545",
            "extra": "mean: 8.463768146324265 usec\nrounds: 30422"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 126099.15420234209,
            "unit": "iter/sec",
            "range": "stddev: 0.000040402615990824704",
            "extra": "mean: 7.9302673069113 usec\nrounds: 39802"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 163651.3170811311,
            "unit": "iter/sec",
            "range": "stddev: 0.000022001496442111535",
            "extra": "mean: 6.110552715590087 usec\nrounds: 42519"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 122262.9726957326,
            "unit": "iter/sec",
            "range": "stddev: 0.000014584739744994137",
            "extra": "mean: 8.179091166780566 usec\nrounds: 38645"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 142359.7480809755,
            "unit": "iter/sec",
            "range": "stddev: 0.00007753706726443828",
            "extra": "mean: 7.024457499258787 usec\nrounds: 10045"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "114298238+ams-amsdal@users.noreply.github.com",
            "name": "ams-amsdal",
            "username": "ams-amsdal"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "f64d1a481e19502e0a132dbe560157d46f52a717",
          "message": "Merge pull request #45 from amsdal/feature/remove-google-site-verification\n\nDelete google72db79d9cefd572a.html",
          "timestamp": "2024-07-25T10:26:51-04:00",
          "tree_id": "b1f9f7457a2326d906c8caeb6885159c805f99b3",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f64d1a481e19502e0a132dbe560157d46f52a717"
        },
        "date": 1721917719778,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 32623.63200102082,
            "unit": "iter/sec",
            "range": "stddev: 0.00009844298060106083",
            "extra": "mean: 30.652626291539494 usec\nrounds: 3569"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 26252.813988401907,
            "unit": "iter/sec",
            "range": "stddev: 0.00014665855019293023",
            "extra": "mean: 38.09115474027983 usec\nrounds: 14431"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 40131.40450741405,
            "unit": "iter/sec",
            "range": "stddev: 0.00006909249661771313",
            "extra": "mean: 24.918141098581675 usec\nrounds: 10406"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 25094.01863893264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000707298894745721",
            "extra": "mean: 39.85013378640474 usec\nrounds: 9366"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 76920.14505132173,
            "unit": "iter/sec",
            "range": "stddev: 0.00007512031607012934",
            "extra": "mean: 13.000495505212479 usec\nrounds: 25110"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 34955.20346776565,
            "unit": "iter/sec",
            "range": "stddev: 0.000030111511061629614",
            "extra": "mean: 28.60804403333432 usec\nrounds: 11090"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 41090.2862664624,
            "unit": "iter/sec",
            "range": "stddev: 0.000045916586571963147",
            "extra": "mean: 24.33665206212479 usec\nrounds: 10032"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 23402.037567078212,
            "unit": "iter/sec",
            "range": "stddev: 0.00012913090968886293",
            "extra": "mean: 42.73132188313344 usec\nrounds: 10319"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 8838.305262121065,
            "unit": "iter/sec",
            "range": "stddev: 0.00006573484567904641",
            "extra": "mean: 113.14386303059356 usec\nrounds: 4988"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 15453.066975869286,
            "unit": "iter/sec",
            "range": "stddev: 0.00013645783402347055",
            "extra": "mean: 64.71207311542419 usec\nrounds: 8284"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 9941.969731597905,
            "unit": "iter/sec",
            "range": "stddev: 0.0001260366012260247",
            "extra": "mean: 100.58368985189786 usec\nrounds: 6552"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6208.34321019113,
            "unit": "iter/sec",
            "range": "stddev: 0.0002091135219158616",
            "extra": "mean: 161.0735692508878 usec\nrounds: 5434"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4700.169734057462,
            "unit": "iter/sec",
            "range": "stddev: 0.0003116426612157177",
            "extra": "mean: 212.75827397338298 usec\nrounds: 4681"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 29552.001264680057,
            "unit": "iter/sec",
            "range": "stddev: 0.00007508818535301532",
            "extra": "mean: 33.83865583395123 usec\nrounds: 15466"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 26922.91891952277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000674533622608622",
            "extra": "mean: 37.143075124549895 usec\nrounds: 14348"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 11994.83261439312,
            "unit": "iter/sec",
            "range": "stddev: 0.0001711210164888216",
            "extra": "mean: 83.36923341473366 usec\nrounds: 4847"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6839.598836328235,
            "unit": "iter/sec",
            "range": "stddev: 0.00015861450875918472",
            "extra": "mean: 146.207405423918 usec\nrounds: 3963"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 8311.865359289797,
            "unit": "iter/sec",
            "range": "stddev: 0.00009933676734981498",
            "extra": "mean: 120.30993727326744 usec\nrounds: 2545"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 8313.84174351685,
            "unit": "iter/sec",
            "range": "stddev: 0.00029537779746459337",
            "extra": "mean: 120.28133693786053 usec\nrounds: 5102"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 28121.880003122857,
            "unit": "iter/sec",
            "range": "stddev: 0.00010252109963991622",
            "extra": "mean: 35.55950028550555 usec\nrounds: 15209"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 18365.799668653213,
            "unit": "iter/sec",
            "range": "stddev: 0.00012146681381348434",
            "extra": "mean: 54.44903124511383 usec\nrounds: 7603"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 20001.550877413047,
            "unit": "iter/sec",
            "range": "stddev: 0.00014064270638331096",
            "extra": "mean: 49.996123107096665 usec\nrounds: 11169"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 8904.013430792313,
            "unit": "iter/sec",
            "range": "stddev: 0.00026406658073214545",
            "extra": "mean: 112.30890516648918 usec\nrounds: 4897"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 7233.920941023495,
            "unit": "iter/sec",
            "range": "stddev: 0.0003842429659353933",
            "extra": "mean: 138.2376180432122 usec\nrounds: 7741"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 57745.317108620075,
            "unit": "iter/sec",
            "range": "stddev: 0.00003706739054853436",
            "extra": "mean: 17.31742156890368 usec\nrounds: 20830"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 38113.757624771795,
            "unit": "iter/sec",
            "range": "stddev: 0.0001271934110989258",
            "extra": "mean: 26.237245087323963 usec\nrounds: 22238"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 41196.55429305175,
            "unit": "iter/sec",
            "range": "stddev: 0.00012707683305680393",
            "extra": "mean: 24.273874773275903 usec\nrounds: 13223"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 70328.44454895632,
            "unit": "iter/sec",
            "range": "stddev: 0.00006564639166130636",
            "extra": "mean: 14.218997823901683 usec\nrounds: 28369"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 69481.02484567456,
            "unit": "iter/sec",
            "range": "stddev: 0.00006592422188002057",
            "extra": "mean: 14.392418681519398 usec\nrounds: 25545"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 76539.3949052151,
            "unit": "iter/sec",
            "range": "stddev: 0.000060957608910931855",
            "extra": "mean: 13.065167306827819 usec\nrounds: 25608"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 104116.13111923254,
            "unit": "iter/sec",
            "range": "stddev: 0.00007242898406220042",
            "extra": "mean: 9.604659616623788 usec\nrounds: 23454"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 55795.844999050416,
            "unit": "iter/sec",
            "range": "stddev: 0.00003648206490287429",
            "extra": "mean: 17.92248150408008 usec\nrounds: 6874"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 69827.47244962389,
            "unit": "iter/sec",
            "range": "stddev: 0.00007592378930564211",
            "extra": "mean: 14.321010984916242 usec\nrounds: 25487"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 29103.007925021764,
            "unit": "iter/sec",
            "range": "stddev: 0.0001229986770795854",
            "extra": "mean: 34.360709469492136 usec\nrounds: 8247"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 15218.268114764003,
            "unit": "iter/sec",
            "range": "stddev: 0.00015147458532029537",
            "extra": "mean: 65.71049954297033 usec\nrounds: 159"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 121418.66769077549,
            "unit": "iter/sec",
            "range": "stddev: 0.00007712955514523484",
            "extra": "mean: 8.235965844615942 usec\nrounds: 33792"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 136441.16609138914,
            "unit": "iter/sec",
            "range": "stddev: 0.000029244069227703194",
            "extra": "mean: 7.329166326020651 usec\nrounds: 44765"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 134679.87328340093,
            "unit": "iter/sec",
            "range": "stddev: 0.00006218009799335726",
            "extra": "mean: 7.425014410993274 usec\nrounds: 40388"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 87441.87229527457,
            "unit": "iter/sec",
            "range": "stddev: 0.00008889959528347398",
            "extra": "mean: 11.436168665547212 usec\nrounds: 38628"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 145987.3373747188,
            "unit": "iter/sec",
            "range": "stddev: 0.000057926715590783576",
            "extra": "mean: 6.849909163239345 usec\nrounds: 51238"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "emil.temirov@litslink.com",
            "name": "Emil Temirov",
            "username": "emilt27"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "2fb3c979e2df611e87c5b52afba753aa15c05e5e",
          "message": "Merge pull request #39 from amsdal/feature/fixes\n\nFeature/fixes",
          "timestamp": "2024-07-29T16:08:48+03:00",
          "tree_id": "25a6e092a5b05cde5437edfb4eb83e3335cf98eb",
          "url": "https://github.com/amsdal/amsdal-glue/commit/2fb3c979e2df611e87c5b52afba753aa15c05e5e"
        },
        "date": 1722258568561,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 22484.11764144981,
            "unit": "iter/sec",
            "range": "stddev: 0.000026470224176300992",
            "extra": "mean: 44.475839165531006 usec\nrounds: 3495"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 23599.681406754713,
            "unit": "iter/sec",
            "range": "stddev: 0.00016793298979082472",
            "extra": "mean: 42.373453385424924 usec\nrounds: 7906"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 44694.21530977206,
            "unit": "iter/sec",
            "range": "stddev: 0.00007679836023685049",
            "extra": "mean: 22.374260137896577 usec\nrounds: 14970"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 22266.81701768566,
            "unit": "iter/sec",
            "range": "stddev: 0.0000806237274017432",
            "extra": "mean: 44.90987639615214 usec\nrounds: 8486"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 74596.03769324816,
            "unit": "iter/sec",
            "range": "stddev: 0.0000649190231428964",
            "extra": "mean: 13.405537759420593 usec\nrounds: 18847"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 25791.922643475486,
            "unit": "iter/sec",
            "range": "stddev: 0.000154690340167072",
            "extra": "mean: 38.77182844501774 usec\nrounds: 10086"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 40575.75261255544,
            "unit": "iter/sec",
            "range": "stddev: 0.00005010469835983779",
            "extra": "mean: 24.64526066955978 usec\nrounds: 9980"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 22926.77242231707,
            "unit": "iter/sec",
            "range": "stddev: 0.00012990133247231083",
            "extra": "mean: 43.6171294231801 usec\nrounds: 10068"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 7074.410438017614,
            "unit": "iter/sec",
            "range": "stddev: 0.00025537872892257536",
            "extra": "mean: 141.3545353017741 usec\nrounds: 3529"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 13750.833096338158,
            "unit": "iter/sec",
            "range": "stddev: 0.00017702509732291086",
            "extra": "mean: 72.72286653426836 usec\nrounds: 9735"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 8458.727308458178,
            "unit": "iter/sec",
            "range": "stddev: 0.00023184798704050362",
            "extra": "mean: 118.22109444290338 usec\nrounds: 4818"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6822.0252965863665,
            "unit": "iter/sec",
            "range": "stddev: 0.00015703975988585",
            "extra": "mean: 146.5840357555379 usec\nrounds: 5473"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4958.09580044271,
            "unit": "iter/sec",
            "range": "stddev: 0.0002123854229947575",
            "extra": "mean: 201.6903344043311 usec\nrounds: 4626"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 29659.74840135209,
            "unit": "iter/sec",
            "range": "stddev: 0.00010509800896114308",
            "extra": "mean: 33.71572767469644 usec\nrounds: 15112"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 23458.501511832033,
            "unit": "iter/sec",
            "range": "stddev: 0.00012526332329632084",
            "extra": "mean: 42.62846880887164 usec\nrounds: 13144"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 12552.159667024122,
            "unit": "iter/sec",
            "range": "stddev: 0.00017739626840131",
            "extra": "mean: 79.66756530568264 usec\nrounds: 7528"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 5388.428282839428,
            "unit": "iter/sec",
            "range": "stddev: 0.00031166889576077293",
            "extra": "mean: 185.582872687516 usec\nrounds: 2578"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 7432.957452922368,
            "unit": "iter/sec",
            "range": "stddev: 0.00024588958583394684",
            "extra": "mean: 134.535951044202 usec\nrounds: 6129"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 9685.52707250155,
            "unit": "iter/sec",
            "range": "stddev: 0.00014083341142645474",
            "extra": "mean: 103.24683339527569 usec\nrounds: 3381"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 22729.83150461602,
            "unit": "iter/sec",
            "range": "stddev: 0.0001529601537982678",
            "extra": "mean: 43.99504676472934 usec\nrounds: 13357"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 15391.366539772565,
            "unit": "iter/sec",
            "range": "stddev: 0.0002020232461248936",
            "extra": "mean: 64.9714888808552 usec\nrounds: 1898"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 21240.12723045117,
            "unit": "iter/sec",
            "range": "stddev: 0.00010000773749780498",
            "extra": "mean: 47.08069726467259 usec\nrounds: 9941"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 10180.168758795766,
            "unit": "iter/sec",
            "range": "stddev: 0.00022690864542584778",
            "extra": "mean: 98.23019870235356 usec\nrounds: 6268"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 9939.277469468365,
            "unit": "iter/sec",
            "range": "stddev: 0.000214414515722828",
            "extra": "mean: 100.61093505758505 usec\nrounds: 6500"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 65021.50872161617,
            "unit": "iter/sec",
            "range": "stddev: 0.000023258957066184266",
            "extra": "mean: 15.379526246944092 usec\nrounds: 10874"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 46627.04569660496,
            "unit": "iter/sec",
            "range": "stddev: 0.00006689345573690543",
            "extra": "mean: 21.446780190768397 usec\nrounds: 23018"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 52827.070283681605,
            "unit": "iter/sec",
            "range": "stddev: 0.00009890790615204147",
            "extra": "mean: 18.929688787017632 usec\nrounds: 16352"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 74718.38032001637,
            "unit": "iter/sec",
            "range": "stddev: 0.0000551728473482919",
            "extra": "mean: 13.383587756011744 usec\nrounds: 21181"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 73559.17540915486,
            "unit": "iter/sec",
            "range": "stddev: 0.00007289879624311125",
            "extra": "mean: 13.59449714379947 usec\nrounds: 24319"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 99247.00215772046,
            "unit": "iter/sec",
            "range": "stddev: 0.000009691079883152603",
            "extra": "mean: 10.075871091912973 usec\nrounds: 27622"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 77510.63981742968,
            "unit": "iter/sec",
            "range": "stddev: 0.00007438151749842457",
            "extra": "mean: 12.901454591981471 usec\nrounds: 30595"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 43467.13360440809,
            "unit": "iter/sec",
            "range": "stddev: 0.00011756048636666978",
            "extra": "mean: 23.005887830123402 usec\nrounds: 11675"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 68531.69480394965,
            "unit": "iter/sec",
            "range": "stddev: 0.00007910726114016165",
            "extra": "mean: 14.591788556531766 usec\nrounds: 29092"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 36629.07829268884,
            "unit": "iter/sec",
            "range": "stddev: 0.00009351865808137353",
            "extra": "mean: 27.30071425792878 usec\nrounds: 10978"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 16753.855697250703,
            "unit": "iter/sec",
            "range": "stddev: 0.000040748242548833527",
            "extra": "mean: 59.687752960896006 usec\nrounds: 245"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 150459.19621737397,
            "unit": "iter/sec",
            "range": "stddev: 0.000015690457509013873",
            "extra": "mean: 6.646320232598232 usec\nrounds: 43017"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 125391.23359279058,
            "unit": "iter/sec",
            "range": "stddev: 0.000039445572629345396",
            "extra": "mean: 7.975039174169951 usec\nrounds: 36609"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 135321.08503892733,
            "unit": "iter/sec",
            "range": "stddev: 0.000033251929863567435",
            "extra": "mean: 7.389831375593343 usec\nrounds: 43684"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 110482.17840283824,
            "unit": "iter/sec",
            "range": "stddev: 0.000041467139463802365",
            "extra": "mean: 9.051233551476665 usec\nrounds: 31548"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 126140.28679283631,
            "unit": "iter/sec",
            "range": "stddev: 0.00005706782107026072",
            "extra": "mean: 7.927681357204521 usec\nrounds: 30856"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "114298238+ams-amsdal@users.noreply.github.com",
            "name": "ams-amsdal",
            "username": "ams-amsdal"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "29e83158fa50c385e4d73b96af08545519f85d16",
          "message": "Merge pull request #50 from amsdal/docs/update-readme-add-benchmarking\n\nUpdate README.md, add benchmarking",
          "timestamp": "2024-07-29T13:20:20-04:00",
          "tree_id": "b7e858680ac1d48a66baa801d4f79e2ef4ef4e65",
          "url": "https://github.com/amsdal/amsdal-glue/commit/29e83158fa50c385e4d73b96af08545519f85d16"
        },
        "date": 1722273686835,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 32527.87504201991,
            "unit": "iter/sec",
            "range": "stddev: 0.00005875354282773542",
            "extra": "mean: 30.74286281253195 usec\nrounds: 3176"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 19504.0899079089,
            "unit": "iter/sec",
            "range": "stddev: 0.00018567755421271492",
            "extra": "mean: 51.27129769815614 usec\nrounds: 15650"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 35040.077052098415,
            "unit": "iter/sec",
            "range": "stddev: 0.00009883828979528649",
            "extra": "mean: 28.538750029378544 usec\nrounds: 14833"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 17411.273425984706,
            "unit": "iter/sec",
            "range": "stddev: 0.0002706365230178179",
            "extra": "mean: 57.43405295718307 usec\nrounds: 8691"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 85860.83109895492,
            "unit": "iter/sec",
            "range": "stddev: 0.00003700821850858133",
            "extra": "mean: 11.646754255703586 usec\nrounds: 25607"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 28225.138942180736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000884900094904229",
            "extra": "mean: 35.429409295327204 usec\nrounds: 11132"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 38757.50524166471,
            "unit": "iter/sec",
            "range": "stddev: 0.00003592860795797779",
            "extra": "mean: 25.80145429290918 usec\nrounds: 9086"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 21750.275159368277,
            "unit": "iter/sec",
            "range": "stddev: 0.00014129819519286682",
            "extra": "mean: 45.97642984618887 usec\nrounds: 10496"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 6354.659502315135,
            "unit": "iter/sec",
            "range": "stddev: 0.00027158642675047343",
            "extra": "mean: 157.36484380251673 usec\nrounds: 3780"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 12684.173498125954,
            "unit": "iter/sec",
            "range": "stddev: 0.0001868005900947699",
            "extra": "mean: 78.83840442167926 usec\nrounds: 8813"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 7775.909183381132,
            "unit": "iter/sec",
            "range": "stddev: 0.00022863238844788683",
            "extra": "mean: 128.60232500364395 usec\nrounds: 2992"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6621.43711313228,
            "unit": "iter/sec",
            "range": "stddev: 0.00021505243916326822",
            "extra": "mean: 151.0246163958429 usec\nrounds: 4346"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 6035.709216365081,
            "unit": "iter/sec",
            "range": "stddev: 0.0001422000871897452",
            "extra": "mean: 165.68061252663122 usec\nrounds: 4813"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 33652.10870504075,
            "unit": "iter/sec",
            "range": "stddev: 0.00004221102750249817",
            "extra": "mean: 29.7158198544096 usec\nrounds: 14461"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 23918.585265512906,
            "unit": "iter/sec",
            "range": "stddev: 0.00011548640898230386",
            "extra": "mean: 41.808492805879006 usec\nrounds: 13898"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 10800.558020448525,
            "unit": "iter/sec",
            "range": "stddev: 0.00014444752866279482",
            "extra": "mean: 92.5878087138383 usec\nrounds: 6402"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 5139.301571308788,
            "unit": "iter/sec",
            "range": "stddev: 0.00038356226284881644",
            "extra": "mean: 194.57896878103173 usec\nrounds: 3201"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 7465.441169932818,
            "unit": "iter/sec",
            "range": "stddev: 0.00015628459475765594",
            "extra": "mean: 133.95055660307335 usec\nrounds: 4044"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 7672.5713416885255,
            "unit": "iter/sec",
            "range": "stddev: 0.00019826315838729743",
            "extra": "mean: 130.33440231002493 usec\nrounds: 5513"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 22465.77751936434,
            "unit": "iter/sec",
            "range": "stddev: 0.00022398484946272124",
            "extra": "mean: 44.512147382304114 usec\nrounds: 11110"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 18722.047475389587,
            "unit": "iter/sec",
            "range": "stddev: 0.00004913514557995949",
            "extra": "mean: 53.412961446365046 usec\nrounds: 8294"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 17893.847655564936,
            "unit": "iter/sec",
            "range": "stddev: 0.00012610153474455806",
            "extra": "mean: 55.88512986411856 usec\nrounds: 11806"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 9544.757367300306,
            "unit": "iter/sec",
            "range": "stddev: 0.00013851081910131645",
            "extra": "mean: 104.76955689056408 usec\nrounds: 997"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 8305.695945484513,
            "unit": "iter/sec",
            "range": "stddev: 0.00020952734655975826",
            "extra": "mean: 120.39930266694407 usec\nrounds: 712"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 50652.908045843134,
            "unit": "iter/sec",
            "range": "stddev: 0.00003759254749927258",
            "extra": "mean: 19.742203134614808 usec\nrounds: 19210"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 37334.84423226655,
            "unit": "iter/sec",
            "range": "stddev: 0.00009364813449121787",
            "extra": "mean: 26.784630298142567 usec\nrounds: 14177"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 51802.86114136831,
            "unit": "iter/sec",
            "range": "stddev: 0.00004703903602636178",
            "extra": "mean: 19.303953062959838 usec\nrounds: 17193"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 59659.00559104312,
            "unit": "iter/sec",
            "range": "stddev: 0.00008521956572027611",
            "extra": "mean: 16.761928733021566 usec\nrounds: 29950"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 66680.00666353133,
            "unit": "iter/sec",
            "range": "stddev: 0.000022426773791231524",
            "extra": "mean: 14.996999101185164 usec\nrounds: 5784"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 77178.79946124053,
            "unit": "iter/sec",
            "range": "stddev: 0.000018419418632764086",
            "extra": "mean: 12.956926085669465 usec\nrounds: 27834"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 107624.46179900164,
            "unit": "iter/sec",
            "range": "stddev: 0.000026310024234998225",
            "extra": "mean: 9.291567951044344 usec\nrounds: 32323"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 44404.6223652924,
            "unit": "iter/sec",
            "range": "stddev: 0.000074839791705145",
            "extra": "mean: 22.52017800700004 usec\nrounds: 16134"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 65055.950137353946,
            "unit": "iter/sec",
            "range": "stddev: 0.00006941281685531903",
            "extra": "mean: 15.371384137633527 usec\nrounds: 27136"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 29359.5385371145,
            "unit": "iter/sec",
            "range": "stddev: 0.0001437843214966477",
            "extra": "mean: 34.060480846313794 usec\nrounds: 11469"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 18842.94618795348,
            "unit": "iter/sec",
            "range": "stddev: 0.00006364630867674075",
            "extra": "mean: 53.07025716813393 usec\nrounds: 317"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 141888.09111635387,
            "unit": "iter/sec",
            "range": "stddev: 0.000027980032319195602",
            "extra": "mean: 7.047807833146197 usec\nrounds: 28132"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 109021.00517643907,
            "unit": "iter/sec",
            "range": "stddev: 0.0000760878115050506",
            "extra": "mean: 9.172544303564298 usec\nrounds: 40937"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 138068.5279183617,
            "unit": "iter/sec",
            "range": "stddev: 0.00004902584920937293",
            "extra": "mean: 7.242780198187441 usec\nrounds: 44449"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 107215.83002215996,
            "unit": "iter/sec",
            "range": "stddev: 0.00003148873667409379",
            "extra": "mean: 9.326980911245236 usec\nrounds: 28634"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 145817.38403809766,
            "unit": "iter/sec",
            "range": "stddev: 0.00003627147961206194",
            "extra": "mean: 6.857892881542371 usec\nrounds: 51611"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "emil.temirov@litslink.com",
            "name": "Emil Temirov",
            "username": "emilt27"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "618919d5e493dca1d6dab0bd1b9ec708a5f8c433",
          "message": "Merge pull request #52 from amsdal/feature/namespaces\n\nFeature/namespaces",
          "timestamp": "2024-07-31T21:21:55+03:00",
          "tree_id": "e185fe510c45d69fdb6816779d62fef82d3af6f3",
          "url": "https://github.com/amsdal/amsdal-glue/commit/618919d5e493dca1d6dab0bd1b9ec708a5f8c433"
        },
        "date": 1722450182841,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 19248.90410335251,
            "unit": "iter/sec",
            "range": "stddev: 0.0000563343746132766",
            "extra": "mean: 51.95100950322849 usec\nrounds: 2085"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 16074.305900439229,
            "unit": "iter/sec",
            "range": "stddev: 0.00008495256930821725",
            "extra": "mean: 62.21108433507384 usec\nrounds: 7954"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 31081.10656246592,
            "unit": "iter/sec",
            "range": "stddev: 0.00011272057264817564",
            "extra": "mean: 32.173886666172216 usec\nrounds: 7369"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 13173.607337776151,
            "unit": "iter/sec",
            "range": "stddev: 0.00007792117139574352",
            "extra": "mean: 75.90935226469341 usec\nrounds: 5727"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 44646.14442454965,
            "unit": "iter/sec",
            "range": "stddev: 0.00005600040270527604",
            "extra": "mean: 22.39835069498472 usec\nrounds: 7125"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 24490.713472045612,
            "unit": "iter/sec",
            "range": "stddev: 0.00010853290090571796",
            "extra": "mean: 40.83180349733086 usec\nrounds: 8210"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 42178.65762224249,
            "unit": "iter/sec",
            "range": "stddev: 0.0000763144233351914",
            "extra": "mean: 23.70867297286057 usec\nrounds: 10501"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 26211.423435169407,
            "unit": "iter/sec",
            "range": "stddev: 0.00009337328352345237",
            "extra": "mean: 38.15130462003987 usec\nrounds: 10952"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 7222.717559138225,
            "unit": "iter/sec",
            "range": "stddev: 0.0003274407268444199",
            "extra": "mean: 138.452042712759 usec\nrounds: 5129"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 12181.493357166479,
            "unit": "iter/sec",
            "range": "stddev: 0.00018796259230848323",
            "extra": "mean: 82.09174119129584 usec\nrounds: 9625"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 9036.300357162465,
            "unit": "iter/sec",
            "range": "stddev: 0.0001507512893120687",
            "extra": "mean: 110.66475885868131 usec\nrounds: 6114"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6963.664824906775,
            "unit": "iter/sec",
            "range": "stddev: 0.0002043324085140978",
            "extra": "mean: 143.6025462373381 usec\nrounds: 4301"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 5871.863571118991,
            "unit": "iter/sec",
            "range": "stddev: 0.00017583918996008342",
            "extra": "mean: 170.3036843223917 usec\nrounds: 4832"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 33563.94015495881,
            "unit": "iter/sec",
            "range": "stddev: 0.00007753216707190285",
            "extra": "mean: 29.793879841972544 usec\nrounds: 15204"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 30690.104149315,
            "unit": "iter/sec",
            "range": "stddev: 0.00007035803562792316",
            "extra": "mean: 32.58379297557124 usec\nrounds: 11325"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 13060.667892315678,
            "unit": "iter/sec",
            "range": "stddev: 0.00017320164548170522",
            "extra": "mean: 76.56576281128442 usec\nrounds: 7320"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6855.672890935261,
            "unit": "iter/sec",
            "range": "stddev: 0.00023632202482523",
            "extra": "mean: 145.86460233863033 usec\nrounds: 4741"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 8137.211077681855,
            "unit": "iter/sec",
            "range": "stddev: 0.00019320676452893516",
            "extra": "mean: 122.8922281176565 usec\nrounds: 4012"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 8714.35399953354,
            "unit": "iter/sec",
            "range": "stddev: 0.0002762350999215143",
            "extra": "mean: 114.75319915320492 usec\nrounds: 5369"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 26235.010780056356,
            "unit": "iter/sec",
            "range": "stddev: 0.00008779042345259716",
            "extra": "mean: 38.11700358668013 usec\nrounds: 14301"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 19305.6745889201,
            "unit": "iter/sec",
            "range": "stddev: 0.0001149576833764381",
            "extra": "mean: 51.79824177570667 usec\nrounds: 5660"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 15796.51599544532,
            "unit": "iter/sec",
            "range": "stddev: 0.00019348273487194102",
            "extra": "mean: 63.30509843362515 usec\nrounds: 11996"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 9143.918134298767,
            "unit": "iter/sec",
            "range": "stddev: 0.00021062089467210104",
            "extra": "mean: 109.36230894817483 usec\nrounds: 6159"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 8269.842856443569,
            "unit": "iter/sec",
            "range": "stddev: 0.00029841026485726474",
            "extra": "mean: 120.9212819831075 usec\nrounds: 4145"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 56076.28802342543,
            "unit": "iter/sec",
            "range": "stddev: 0.00010626571806805796",
            "extra": "mean: 17.832849413681906 usec\nrounds: 13330"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 49626.80382633008,
            "unit": "iter/sec",
            "range": "stddev: 0.00008704633082136956",
            "extra": "mean: 20.150401051405986 usec\nrounds: 21262"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 54815.14634202156,
            "unit": "iter/sec",
            "range": "stddev: 0.00008633587892623331",
            "extra": "mean: 18.24313290637692 usec\nrounds: 9968"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 79492.59016731883,
            "unit": "iter/sec",
            "range": "stddev: 0.00007851390001982571",
            "extra": "mean: 12.579788856988614 usec\nrounds: 14867"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 59437.26944664233,
            "unit": "iter/sec",
            "range": "stddev: 0.00010618111057224825",
            "extra": "mean: 16.824460634042318 usec\nrounds: 24463"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 83623.86449576565,
            "unit": "iter/sec",
            "range": "stddev: 0.00003363563630132365",
            "extra": "mean: 11.958308863501944 usec\nrounds: 15324"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 109898.63788373354,
            "unit": "iter/sec",
            "range": "stddev: 0.00006472600143068653",
            "extra": "mean: 9.099293851648486 usec\nrounds: 30134"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 60521.810075832545,
            "unit": "iter/sec",
            "range": "stddev: 0.000040815805916787916",
            "extra": "mean: 16.52296913702715 usec\nrounds: 16346"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 92079.69822166866,
            "unit": "iter/sec",
            "range": "stddev: 0.000014496663617768103",
            "extra": "mean: 10.860157225891895 usec\nrounds: 27045"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 38197.05860362027,
            "unit": "iter/sec",
            "range": "stddev: 0.00007719119036294523",
            "extra": "mean: 26.180026330750536 usec\nrounds: 12009"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 7411.270507341852,
            "unit": "iter/sec",
            "range": "stddev: 0.00039273167706835397",
            "extra": "mean: 134.92963170206332 usec\nrounds: 166"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 127775.43875486069,
            "unit": "iter/sec",
            "range": "stddev: 0.00003929658150607452",
            "extra": "mean: 7.82623021877089 usec\nrounds: 42456"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 96732.0780048701,
            "unit": "iter/sec",
            "range": "stddev: 0.00007896070371736273",
            "extra": "mean: 10.337832295401054 usec\nrounds: 38481"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 112402.74473404075,
            "unit": "iter/sec",
            "range": "stddev: 0.00011196051191219644",
            "extra": "mean: 8.8965799043976 usec\nrounds: 43728"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 89368.08693824294,
            "unit": "iter/sec",
            "range": "stddev: 0.00008575360260262507",
            "extra": "mean: 11.189676698473379 usec\nrounds: 24960"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 126882.3725478469,
            "unit": "iter/sec",
            "range": "stddev: 0.00007608407839070851",
            "extra": "mean: 7.881315425615197 usec\nrounds: 54892"
          }
        ]
      }
    ]
  }
}