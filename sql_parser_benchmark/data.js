window.BENCHMARK_DATA = {
  "lastUpdate": 1750968917082,
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
          "id": "97db4e2c17fb242b15c8543527393b4c381bef62",
          "message": "Merge pull request #54 from amsdal/fixes/psycopg-dep-fix-during-import\n\nFixed psycopg dep import in amsdal_glue.__init__",
          "timestamp": "2024-08-01T14:54:57+03:00",
          "tree_id": "3bfea135dc0031962b5987ac98372a912117d853",
          "url": "https://github.com/amsdal/amsdal-glue/commit/97db4e2c17fb242b15c8543527393b4c381bef62"
        },
        "date": 1722513335888,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 21010.203822346026,
            "unit": "iter/sec",
            "range": "stddev: 0.00020121594412169077",
            "extra": "mean: 47.595920937064896 usec\nrounds: 2495"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 14849.03330426118,
            "unit": "iter/sec",
            "range": "stddev: 0.00018709595874479443",
            "extra": "mean: 67.34445128579739 usec\nrounds: 2942"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 27305.306112013062,
            "unit": "iter/sec",
            "range": "stddev: 0.00009344436729064506",
            "extra": "mean: 36.6229184868961 usec\nrounds: 11042"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 16159.008549121394,
            "unit": "iter/sec",
            "range": "stddev: 0.00011754146487318921",
            "extra": "mean: 61.884984896203456 usec\nrounds: 10031"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 72038.91751532674,
            "unit": "iter/sec",
            "range": "stddev: 0.00009927420124160201",
            "extra": "mean: 13.881385707763355 usec\nrounds: 22481"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 28647.831380261443,
            "unit": "iter/sec",
            "range": "stddev: 0.00015271158661850522",
            "extra": "mean: 34.90665616975835 usec\nrounds: 11024"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 30055.951278113527,
            "unit": "iter/sec",
            "range": "stddev: 0.00016474169333920228",
            "extra": "mean: 33.27128097682907 usec\nrounds: 6924"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 21649.564601882827,
            "unit": "iter/sec",
            "range": "stddev: 0.00016518469971379618",
            "extra": "mean: 46.19030536591169 usec\nrounds: 9533"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 9302.520792427018,
            "unit": "iter/sec",
            "range": "stddev: 0.000055737182600545",
            "extra": "mean: 107.49774413985493 usec\nrounds: 3425"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 16473.68087317736,
            "unit": "iter/sec",
            "range": "stddev: 0.00005802854153918838",
            "extra": "mean: 60.70288769695737 usec\nrounds: 8938"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 10309.214635172999,
            "unit": "iter/sec",
            "range": "stddev: 0.00015429282700380256",
            "extra": "mean: 97.00059950136242 usec\nrounds: 5567"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6786.538488029534,
            "unit": "iter/sec",
            "range": "stddev: 0.00027367528107706556",
            "extra": "mean: 147.35052365264772 usec\nrounds: 5271"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4675.131334038994,
            "unit": "iter/sec",
            "range": "stddev: 0.0002640714852055433",
            "extra": "mean: 213.89773432013263 usec\nrounds: 4408"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 30222.696926721157,
            "unit": "iter/sec",
            "range": "stddev: 0.00006328494079101486",
            "extra": "mean: 33.08771558093011 usec\nrounds: 14400"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 21622.24936021613,
            "unit": "iter/sec",
            "range": "stddev: 0.00015074461366349458",
            "extra": "mean: 46.24865726689614 usec\nrounds: 14397"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 12650.493072829806,
            "unit": "iter/sec",
            "range": "stddev: 0.00018610982563143925",
            "extra": "mean: 79.04830224742447 usec\nrounds: 7281"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6260.392692651896,
            "unit": "iter/sec",
            "range": "stddev: 0.0001998814834642279",
            "extra": "mean: 159.73438873471068 usec\nrounds: 4191"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 6349.741030082705,
            "unit": "iter/sec",
            "range": "stddev: 0.00028477581137110455",
            "extra": "mean: 157.48673768935976 usec\nrounds: 5733"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 8975.031223710057,
            "unit": "iter/sec",
            "range": "stddev: 0.00018879003698400116",
            "extra": "mean: 111.4202251863169 usec\nrounds: 5316"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 26282.880057477963,
            "unit": "iter/sec",
            "range": "stddev: 0.00007216633192025029",
            "extra": "mean: 38.04758069941736 usec\nrounds: 15288"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 13475.171301272712,
            "unit": "iter/sec",
            "range": "stddev: 0.0002692549969547101",
            "extra": "mean: 74.21055937934914 usec\nrounds: 5252"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 18216.38766277472,
            "unit": "iter/sec",
            "range": "stddev: 0.00014071544500609068",
            "extra": "mean: 54.89562576907084 usec\nrounds: 11703"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 9806.249216070033,
            "unit": "iter/sec",
            "range": "stddev: 0.0002843833613054732",
            "extra": "mean: 101.9757889042067 usec\nrounds: 6146"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 9115.875284385753,
            "unit": "iter/sec",
            "range": "stddev: 0.0002045040430857463",
            "extra": "mean: 109.69873641348113 usec\nrounds: 5139"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 48611.28216852855,
            "unit": "iter/sec",
            "range": "stddev: 0.00009726628274918218",
            "extra": "mean: 20.57135618297701 usec\nrounds: 21762"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 46622.854240568224,
            "unit": "iter/sec",
            "range": "stddev: 0.00010926359590727332",
            "extra": "mean: 21.44870828457053 usec\nrounds: 16034"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 48474.23728598007,
            "unit": "iter/sec",
            "range": "stddev: 0.0000955969312097047",
            "extra": "mean: 20.629514892629874 usec\nrounds: 17114"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 81887.4525604211,
            "unit": "iter/sec",
            "range": "stddev: 0.00003484261742510297",
            "extra": "mean: 12.211883124122643 usec\nrounds: 28426"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 76834.29345782039,
            "unit": "iter/sec",
            "range": "stddev: 0.00002786359685757489",
            "extra": "mean: 13.015021743500103 usec\nrounds: 27085"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 86789.44467621796,
            "unit": "iter/sec",
            "range": "stddev: 0.0000475334065989575",
            "extra": "mean: 11.522138478137078 usec\nrounds: 20419"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 124992.72929155357,
            "unit": "iter/sec",
            "range": "stddev: 0.000040589939641865754",
            "extra": "mean: 8.000465352408105 usec\nrounds: 25620"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 56283.27281422179,
            "unit": "iter/sec",
            "range": "stddev: 0.00009706567772705752",
            "extra": "mean: 17.767268142006795 usec\nrounds: 16990"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 88144.42720905964,
            "unit": "iter/sec",
            "range": "stddev: 0.000057301324728284165",
            "extra": "mean: 11.34501671476309 usec\nrounds: 23476"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 47974.71874146943,
            "unit": "iter/sec",
            "range": "stddev: 0.000010623880728456094",
            "extra": "mean: 20.84431188411738 usec\nrounds: 12539"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 26029.341852491536,
            "unit": "iter/sec",
            "range": "stddev: 0.000004018225969527486",
            "extra": "mean: 38.41818228317131 usec\nrounds: 318"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 187683.23165047582,
            "unit": "iter/sec",
            "range": "stddev: 0.000005919243516289266",
            "extra": "mean: 5.328126499133972 usec\nrounds: 39167"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 169650.47830051917,
            "unit": "iter/sec",
            "range": "stddev: 0.000007513154778582019",
            "extra": "mean: 5.89447203460634 usec\nrounds: 35270"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 163576.71266655595,
            "unit": "iter/sec",
            "range": "stddev: 0.000036693407146329315",
            "extra": "mean: 6.113339629452371 usec\nrounds: 43779"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 95994.41588281708,
            "unit": "iter/sec",
            "range": "stddev: 0.00007658207677816158",
            "extra": "mean: 10.417272617406478 usec\nrounds: 40628"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 151998.99663550255,
            "unit": "iter/sec",
            "range": "stddev: 0.0000305288995901741",
            "extra": "mean: 6.578990796880229 usec\nrounds: 53306"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "fbbf6b1cf9b65c33adba813f367f662d7542a971",
          "message": "Merge pull request #53 from amsdal/change_logs\n\nadded change logs",
          "timestamp": "2024-08-01T18:43:48+03:00",
          "tree_id": "6a9e3397c92c31f45a61d1143859e60c5dca7d94",
          "url": "https://github.com/amsdal/amsdal-glue/commit/fbbf6b1cf9b65c33adba813f367f662d7542a971"
        },
        "date": 1722527065735,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 17212.680609070998,
            "unit": "iter/sec",
            "range": "stddev: 0.00019168766799494707",
            "extra": "mean: 58.096703396274314 usec\nrounds: 3149"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 14665.038338941764,
            "unit": "iter/sec",
            "range": "stddev: 0.00018743342865799528",
            "extra": "mean: 68.18938872765064 usec\nrounds: 7773"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 24089.144523787945,
            "unit": "iter/sec",
            "range": "stddev: 0.00007127722428226897",
            "extra": "mean: 41.5124745925495 usec\nrounds: 9214"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 14463.31880445068,
            "unit": "iter/sec",
            "range": "stddev: 0.00017997486621074097",
            "extra": "mean: 69.14042437426451 usec\nrounds: 6333"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 68659.6196991557,
            "unit": "iter/sec",
            "range": "stddev: 0.000037481586236966045",
            "extra": "mean: 14.564601499129727 usec\nrounds: 15021"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 25351.42127314331,
            "unit": "iter/sec",
            "range": "stddev: 0.00015217798719456153",
            "extra": "mean: 39.44552020282098 usec\nrounds: 10673"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 38832.89158139159,
            "unit": "iter/sec",
            "range": "stddev: 0.00007833031701774928",
            "extra": "mean: 25.751365898263213 usec\nrounds: 7348"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 20424.962345324766,
            "unit": "iter/sec",
            "range": "stddev: 0.00020263828920885323",
            "extra": "mean: 48.9596985831848 usec\nrounds: 8615"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 6313.437375476308,
            "unit": "iter/sec",
            "range": "stddev: 0.00024555983742161655",
            "extra": "mean: 158.3923210966445 usec\nrounds: 2100"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 12471.65525437947,
            "unit": "iter/sec",
            "range": "stddev: 0.00016864581578310408",
            "extra": "mean: 80.18181866026534 usec\nrounds: 9613"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 8444.65338748258,
            "unit": "iter/sec",
            "range": "stddev: 0.00014477229208324926",
            "extra": "mean: 118.41812258183259 usec\nrounds: 6840"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 5508.709020821393,
            "unit": "iter/sec",
            "range": "stddev: 0.0002245959432728938",
            "extra": "mean: 181.53073546275127 usec\nrounds: 3318"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4407.9006247344605,
            "unit": "iter/sec",
            "range": "stddev: 0.00031433256386789396",
            "extra": "mean: 226.86536860395796 usec\nrounds: 3693"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 31841.54094672451,
            "unit": "iter/sec",
            "range": "stddev: 0.00010405306712285323",
            "extra": "mean: 31.405515256725295 usec\nrounds: 13508"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 27786.19532306699,
            "unit": "iter/sec",
            "range": "stddev: 0.0001145988588270872",
            "extra": "mean: 35.9890941661178 usec\nrounds: 11970"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 11295.524643944687,
            "unit": "iter/sec",
            "range": "stddev: 0.00018014515663578013",
            "extra": "mean: 88.5306377102263 usec\nrounds: 6971"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6182.3596489478805,
            "unit": "iter/sec",
            "range": "stddev: 0.00019773931407162718",
            "extra": "mean: 161.7505381088887 usec\nrounds: 4169"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 6563.547083372922,
            "unit": "iter/sec",
            "range": "stddev: 0.00028593505299160266",
            "extra": "mean: 152.35664303121186 usec\nrounds: 6099"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 7825.417228799748,
            "unit": "iter/sec",
            "range": "stddev: 0.00028285347332891947",
            "extra": "mean: 127.78871346561782 usec\nrounds: 2825"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 28868.379572519396,
            "unit": "iter/sec",
            "range": "stddev: 0.00007330822787433013",
            "extra": "mean: 34.63997684691411 usec\nrounds: 15024"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 18522.393271241403,
            "unit": "iter/sec",
            "range": "stddev: 0.00010934747069450508",
            "extra": "mean: 53.98870358468413 usec\nrounds: 7274"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 19590.601657767624,
            "unit": "iter/sec",
            "range": "stddev: 0.00013020751010495057",
            "extra": "mean: 51.04488455582999 usec\nrounds: 11485"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 10770.484191947975,
            "unit": "iter/sec",
            "range": "stddev: 0.00010833076109141353",
            "extra": "mean: 92.8463365414529 usec\nrounds: 5714"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 7221.897292723702,
            "unit": "iter/sec",
            "range": "stddev: 0.0003330408721895705",
            "extra": "mean: 138.46776815941882 usec\nrounds: 7096"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 45480.85303642456,
            "unit": "iter/sec",
            "range": "stddev: 0.00005820326065522163",
            "extra": "mean: 21.987274495470064 usec\nrounds: 21972"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 35355.23996194364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000688436139958433",
            "extra": "mean: 28.284350525591094 usec\nrounds: 19193"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 49402.86364236602,
            "unit": "iter/sec",
            "range": "stddev: 0.000027854350793292436",
            "extra": "mean: 20.241741596987872 usec\nrounds: 4193"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 61661.86667737725,
            "unit": "iter/sec",
            "range": "stddev: 0.00003654673728345403",
            "extra": "mean: 16.21747854686475 usec\nrounds: 29488"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 52582.69226924372,
            "unit": "iter/sec",
            "range": "stddev: 0.00006484766769183965",
            "extra": "mean: 19.017664498417336 usec\nrounds: 23014"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 66968.97091490061,
            "unit": "iter/sec",
            "range": "stddev: 0.00006547520271227098",
            "extra": "mean: 14.932288585869546 usec\nrounds: 20261"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 99288.82740456426,
            "unit": "iter/sec",
            "range": "stddev: 0.000019403751497435787",
            "extra": "mean: 10.071626648639729 usec\nrounds: 24486"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 46211.03567201297,
            "unit": "iter/sec",
            "range": "stddev: 0.00006845159673458708",
            "extra": "mean: 21.63985259057146 usec\nrounds: 16898"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 64259.27638879676,
            "unit": "iter/sec",
            "range": "stddev: 0.00005146476031254018",
            "extra": "mean: 15.561955505841087 usec\nrounds: 27090"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 32894.13539183422,
            "unit": "iter/sec",
            "range": "stddev: 0.00009097547707497648",
            "extra": "mean: 30.40055584644563 usec\nrounds: 12217"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 18191.98535936588,
            "unit": "iter/sec",
            "range": "stddev: 0.00004339935566449514",
            "extra": "mean: 54.969261476739504 usec\nrounds: 244"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 155394.310560963,
            "unit": "iter/sec",
            "range": "stddev: 0.000016843797588069207",
            "extra": "mean: 6.435242039364679 usec\nrounds: 35931"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 130449.56837185824,
            "unit": "iter/sec",
            "range": "stddev: 0.000013112193286040863",
            "extra": "mean: 7.665797690870161 usec\nrounds: 12104"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 154272.87403352483,
            "unit": "iter/sec",
            "range": "stddev: 0.000021568470684462845",
            "extra": "mean: 6.482020940263881 usec\nrounds: 13554"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 97713.13736083641,
            "unit": "iter/sec",
            "range": "stddev: 0.00002965160022949109",
            "extra": "mean: 10.234038400662403 usec\nrounds: 40447"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 188947.78356469638,
            "unit": "iter/sec",
            "range": "stddev: 0.000006840604207624152",
            "extra": "mean: 5.292467480348064 usec\nrounds: 53649"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "46465c1fcde6293d2ae88e92b522821acc006899",
          "message": "Merge pull request #55 from amsdal/change_logs\n\nadded towncrier to dependencies",
          "timestamp": "2024-08-02T10:26:04+03:00",
          "tree_id": "176091e924bdb9adf9d502daa72462cde83e38a6",
          "url": "https://github.com/amsdal/amsdal-glue/commit/46465c1fcde6293d2ae88e92b522821acc006899"
        },
        "date": 1722583605113,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 36819.53834754829,
            "unit": "iter/sec",
            "range": "stddev: 0.0000607449442165933",
            "extra": "mean: 27.159493162591144 usec\nrounds: 4188"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 25628.666637580285,
            "unit": "iter/sec",
            "range": "stddev: 0.00010313755283085252",
            "extra": "mean: 39.018807109288396 usec\nrounds: 14029"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 41983.69131041372,
            "unit": "iter/sec",
            "range": "stddev: 0.000030318279238581155",
            "extra": "mean: 23.818772689764845 usec\nrounds: 6189"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 21086.4761311917,
            "unit": "iter/sec",
            "range": "stddev: 0.00008386458915699724",
            "extra": "mean: 47.42376079238637 usec\nrounds: 6640"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 77472.6422748541,
            "unit": "iter/sec",
            "range": "stddev: 0.00003774081455257268",
            "extra": "mean: 12.907782291098878 usec\nrounds: 26746"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 27501.83332958872,
            "unit": "iter/sec",
            "range": "stddev: 0.00006967587943485042",
            "extra": "mean: 36.3612122877684 usec\nrounds: 11272"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 36161.76858269923,
            "unit": "iter/sec",
            "range": "stddev: 0.000032344970569868365",
            "extra": "mean: 27.653514725450318 usec\nrounds: 8101"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 22899.295882244227,
            "unit": "iter/sec",
            "range": "stddev: 0.00009017101630937941",
            "extra": "mean: 43.66946499762838 usec\nrounds: 5842"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 7732.45785555926,
            "unit": "iter/sec",
            "range": "stddev: 0.00017754302272612803",
            "extra": "mean: 129.32498549359036 usec\nrounds: 5039"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 11257.200330938762,
            "unit": "iter/sec",
            "range": "stddev: 0.00022959794505831828",
            "extra": "mean: 88.83203377412116 usec\nrounds: 9322"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 7598.198830333727,
            "unit": "iter/sec",
            "range": "stddev: 0.0002682818615330126",
            "extra": "mean: 131.61013844593984 usec\nrounds: 4292"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 5777.935489445203,
            "unit": "iter/sec",
            "range": "stddev: 0.00026611615828712196",
            "extra": "mean: 173.07219885489238 usec\nrounds: 5600"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4619.8062140782,
            "unit": "iter/sec",
            "range": "stddev: 0.0003189739291990802",
            "extra": "mean: 216.45929583640168 usec\nrounds: 4672"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 23155.089421804212,
            "unit": "iter/sec",
            "range": "stddev: 0.0001631925472693326",
            "extra": "mean: 43.187049800737995 usec\nrounds: 12569"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 24701.34125128435,
            "unit": "iter/sec",
            "range": "stddev: 0.0000852658184803155",
            "extra": "mean: 40.483631630651026 usec\nrounds: 11687"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 13665.939238202931,
            "unit": "iter/sec",
            "range": "stddev: 0.00006169493925709138",
            "extra": "mean: 73.17462653459741 usec\nrounds: 7422"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 8001.404721545464,
            "unit": "iter/sec",
            "range": "stddev: 0.00014171468907125218",
            "extra": "mean: 124.978055079165 usec\nrounds: 3792"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 9757.198775266668,
            "unit": "iter/sec",
            "range": "stddev: 0.00011790696287061136",
            "extra": "mean: 102.48843167312327 usec\nrounds: 5802"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 6672.371212632084,
            "unit": "iter/sec",
            "range": "stddev: 0.0003848314987348931",
            "extra": "mean: 149.87175745060574 usec\nrounds: 4595"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 27305.312752388625,
            "unit": "iter/sec",
            "range": "stddev: 0.00004165735839427549",
            "extra": "mean: 36.62290958057317 usec\nrounds: 1312"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 19314.35547587629,
            "unit": "iter/sec",
            "range": "stddev: 0.0000921354840045858",
            "extra": "mean: 51.774960922149546 usec\nrounds: 5930"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 20803.56462041853,
            "unit": "iter/sec",
            "range": "stddev: 0.00008187618278211147",
            "extra": "mean: 48.068685258799746 usec\nrounds: 11365"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 8886.7484311758,
            "unit": "iter/sec",
            "range": "stddev: 0.0002993591310940758",
            "extra": "mean: 112.52709669285538 usec\nrounds: 5724"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 8917.717225458107,
            "unit": "iter/sec",
            "range": "stddev: 0.0002377571887601434",
            "extra": "mean: 112.13632084511735 usec\nrounds: 3704"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 53874.184157733456,
            "unit": "iter/sec",
            "range": "stddev: 0.00007105118468110295",
            "extra": "mean: 18.561766004143813 usec\nrounds: 21282"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 43415.15030048309,
            "unit": "iter/sec",
            "range": "stddev: 0.00007494692021646215",
            "extra": "mean: 23.03343402196797 usec\nrounds: 14900"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 33243.01543189556,
            "unit": "iter/sec",
            "range": "stddev: 0.0001674313775858871",
            "extra": "mean: 30.08150695741438 usec\nrounds: 1140"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 74796.05638110326,
            "unit": "iter/sec",
            "range": "stddev: 0.00007180548077492014",
            "extra": "mean: 13.36968883633073 usec\nrounds: 23478"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 68418.27828084005,
            "unit": "iter/sec",
            "range": "stddev: 0.000057873632083524044",
            "extra": "mean: 14.615977266999444 usec\nrounds: 24986"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 81592.8907072709,
            "unit": "iter/sec",
            "range": "stddev: 0.0000521355154378994",
            "extra": "mean: 12.25596974603681 usec\nrounds: 30855"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 94406.18057133543,
            "unit": "iter/sec",
            "range": "stddev: 0.00006462656879378855",
            "extra": "mean: 10.592526823435861 usec\nrounds: 31525"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 42063.53043674769,
            "unit": "iter/sec",
            "range": "stddev: 0.00009389661013655057",
            "extra": "mean: 23.773563217755406 usec\nrounds: 16932"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 59365.72295251232,
            "unit": "iter/sec",
            "range": "stddev: 0.0000996040763777784",
            "extra": "mean: 16.844737169290728 usec\nrounds: 27758"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 36206.85567907706,
            "unit": "iter/sec",
            "range": "stddev: 0.00010364672481913865",
            "extra": "mean: 27.61907879721995 usec\nrounds: 11797"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 24001.23814396153,
            "unit": "iter/sec",
            "range": "stddev: 0.000015583973315685783",
            "extra": "mean: 41.66451722206631 usec\nrounds: 337"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 122016.64448734379,
            "unit": "iter/sec",
            "range": "stddev: 0.00007711531296151918",
            "extra": "mean: 8.19560318349621 usec\nrounds: 44081"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 143914.77515685468,
            "unit": "iter/sec",
            "range": "stddev: 0.000042832387015063164",
            "extra": "mean: 6.9485568727052955 usec\nrounds: 38495"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 132347.66151534757,
            "unit": "iter/sec",
            "range": "stddev: 0.00007052301253791351",
            "extra": "mean: 7.555856964530015 usec\nrounds: 43543"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 76818.26398859473,
            "unit": "iter/sec",
            "range": "stddev: 0.00009036102220045412",
            "extra": "mean: 13.017737554554355 usec\nrounds: 35104"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 122822.112365254,
            "unit": "iter/sec",
            "range": "stddev: 0.00006923462184619691",
            "extra": "mean: 8.14185638678933 usec\nrounds: 44139"
          }
        ]
      },
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
          "id": "01711e3ce02984df7d812fd0be75d8502cb2d1de",
          "message": "Merge pull request #46 from amsdal/feature/api-server\n\nAPI Server",
          "timestamp": "2024-08-02T14:53:45+03:00",
          "tree_id": "b8134454a78d12f92b4dc6b2369b31eda6ae3581",
          "url": "https://github.com/amsdal/amsdal-glue/commit/01711e3ce02984df7d812fd0be75d8502cb2d1de"
        },
        "date": 1722599664698,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 19265.44836528672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000586451439751964",
            "extra": "mean: 51.906396417009496 usec\nrounds: 3112"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 14580.611465628985,
            "unit": "iter/sec",
            "range": "stddev: 0.0003468194191379923",
            "extra": "mean: 68.58422929362803 usec\nrounds: 10166"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 23010.184141612743,
            "unit": "iter/sec",
            "range": "stddev: 0.00006836136238562043",
            "extra": "mean: 43.45901770475409 usec\nrounds: 8685"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 13993.904301087648,
            "unit": "iter/sec",
            "range": "stddev: 0.00022160971568064916",
            "extra": "mean: 71.45968548050433 usec\nrounds: 6600"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 28320.944550534048,
            "unit": "iter/sec",
            "range": "stddev: 0.0002746511147664166",
            "extra": "mean: 35.309556791641086 usec\nrounds: 19392"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 19856.3437192706,
            "unit": "iter/sec",
            "range": "stddev: 0.0001830073163510805",
            "extra": "mean: 50.36173900583212 usec\nrounds: 7591"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 24891.71574836743,
            "unit": "iter/sec",
            "range": "stddev: 0.0001969057447568077",
            "extra": "mean: 40.17400849781063 usec\nrounds: 6686"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 21084.11415630465,
            "unit": "iter/sec",
            "range": "stddev: 0.00015220645170124973",
            "extra": "mean: 47.42907349991634 usec\nrounds: 9948"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 6402.0155661282515,
            "unit": "iter/sec",
            "range": "stddev: 0.0002935799047026724",
            "extra": "mean: 156.2008073349266 usec\nrounds: 4461"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 12694.081220912334,
            "unit": "iter/sec",
            "range": "stddev: 0.00021730438119233074",
            "extra": "mean: 78.77687109426964 usec\nrounds: 9326"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 9765.213163431834,
            "unit": "iter/sec",
            "range": "stddev: 0.00018688196098959312",
            "extra": "mean: 102.40431860153735 usec\nrounds: 6591"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 7083.062109259604,
            "unit": "iter/sec",
            "range": "stddev: 0.00019069005573164424",
            "extra": "mean: 141.1818765068729 usec\nrounds: 5627"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 4710.328364442571,
            "unit": "iter/sec",
            "range": "stddev: 0.0002546087653669575",
            "extra": "mean: 212.2994242925444 usec\nrounds: 4674"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 27257.73725897187,
            "unit": "iter/sec",
            "range": "stddev: 0.00011031948641193384",
            "extra": "mean: 36.68683099037689 usec\nrounds: 15090"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 26571.62469848345,
            "unit": "iter/sec",
            "range": "stddev: 0.00017080170806457767",
            "extra": "mean: 37.63413081989954 usec\nrounds: 13753"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 13228.408206327673,
            "unit": "iter/sec",
            "range": "stddev: 0.00019013697635271822",
            "extra": "mean: 75.59488521995112 usec\nrounds: 6626"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 6777.538864198466,
            "unit": "iter/sec",
            "range": "stddev: 0.0002910546871038791",
            "extra": "mean: 147.5461845423535 usec\nrounds: 3838"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 6364.760865039729,
            "unit": "iter/sec",
            "range": "stddev: 0.00023309176947938504",
            "extra": "mean: 157.11509374889263 usec\nrounds: 2857"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 7601.393022160617,
            "unit": "iter/sec",
            "range": "stddev: 0.0002610094156712475",
            "extra": "mean: 131.55483436847217 usec\nrounds: 5212"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 21686.978975332004,
            "unit": "iter/sec",
            "range": "stddev: 0.00015607414406020595",
            "extra": "mean: 46.11061785680046 usec\nrounds: 15325"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 15115.586963246757,
            "unit": "iter/sec",
            "range": "stddev: 0.00019394720690760287",
            "extra": "mean: 66.15687518000325 usec\nrounds: 6652"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 19224.866323243517,
            "unit": "iter/sec",
            "range": "stddev: 0.00010001846534663569",
            "extra": "mean: 52.01596636284363 usec\nrounds: 4570"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 10724.70186928317,
            "unit": "iter/sec",
            "range": "stddev: 0.000098353662066876",
            "extra": "mean: 93.2426851756243 usec\nrounds: 5543"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 8964.049087762385,
            "unit": "iter/sec",
            "range": "stddev: 0.00018834828855010316",
            "extra": "mean: 111.55672957717157 usec\nrounds: 5885"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 47410.385776201874,
            "unit": "iter/sec",
            "range": "stddev: 0.0001427374053461182",
            "extra": "mean: 21.092424869108747 usec\nrounds: 16236"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 39224.54898807771,
            "unit": "iter/sec",
            "range": "stddev: 0.00010246112602064941",
            "extra": "mean: 25.49423832263692 usec\nrounds: 13584"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 44059.94302299115,
            "unit": "iter/sec",
            "range": "stddev: 0.00007395690554874842",
            "extra": "mean: 22.69635254585292 usec\nrounds: 15154"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 57883.13948580403,
            "unit": "iter/sec",
            "range": "stddev: 0.00006198479297931112",
            "extra": "mean: 17.276188003680282 usec\nrounds: 26881"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 52007.53120871838,
            "unit": "iter/sec",
            "range": "stddev: 0.00008882027973676982",
            "extra": "mean: 19.227984423770593 usec\nrounds: 24320"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 72373.99648258396,
            "unit": "iter/sec",
            "range": "stddev: 0.00009859258749598608",
            "extra": "mean: 13.81711731561818 usec\nrounds: 25539"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 94084.19664882579,
            "unit": "iter/sec",
            "range": "stddev: 0.0000908732941824304",
            "extra": "mean: 10.62877758028325 usec\nrounds: 28639"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 55259.75688753642,
            "unit": "iter/sec",
            "range": "stddev: 0.000030926708002015706",
            "extra": "mean: 18.096351781553807 usec\nrounds: 15543"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 65916.87436159968,
            "unit": "iter/sec",
            "range": "stddev: 0.00010099918126997311",
            "extra": "mean: 15.170622237248507 usec\nrounds: 18810"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 34400.31895798463,
            "unit": "iter/sec",
            "range": "stddev: 0.0001115425984984282",
            "extra": "mean: 29.06949790847479 usec\nrounds: 10799"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 20805.763122981978,
            "unit": "iter/sec",
            "range": "stddev: 0.00003988381306865032",
            "extra": "mean: 48.06360593884698 usec\nrounds: 307"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 148783.26910393903,
            "unit": "iter/sec",
            "range": "stddev: 0.00002486512748609255",
            "extra": "mean: 6.721185829714539 usec\nrounds: 32031"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 105271.48530770619,
            "unit": "iter/sec",
            "range": "stddev: 0.00010358716080921178",
            "extra": "mean: 9.499248510430176 usec\nrounds: 42703"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 168782.0441999117,
            "unit": "iter/sec",
            "range": "stddev: 0.00000989097799363989",
            "extra": "mean: 5.92480085627807 usec\nrounds: 42496"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 115558.69593787089,
            "unit": "iter/sec",
            "range": "stddev: 0.000014515664955929833",
            "extra": "mean: 8.653610979978877 usec\nrounds: 18240"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 152290.96187781706,
            "unit": "iter/sec",
            "range": "stddev: 0.000046094179057983734",
            "extra": "mean: 6.5663778576846825 usec\nrounds: 49890"
          }
        ]
      },
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
          "id": "663bf67cf3a3493501ae6338421bfad97dc11ee6",
          "message": "Merge pull request #56 from amsdal/fix/dependencies\n\nFix dependencies",
          "timestamp": "2024-08-05T14:59:09+03:00",
          "tree_id": "36944311e3069bcbb2719ff549f4928080042170",
          "url": "https://github.com/amsdal/amsdal-glue/commit/663bf67cf3a3493501ae6338421bfad97dc11ee6"
        },
        "date": 1722859218097,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 24837.961783340987,
            "unit": "iter/sec",
            "range": "stddev: 0.000005622312002724895",
            "extra": "mean: 40.260952517879616 usec\nrounds: 3812"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 19977.170452666498,
            "unit": "iter/sec",
            "range": "stddev: 0.00000748679968679244",
            "extra": "mean: 50.05713909131324 usec\nrounds: 10094"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 46560.14496688196,
            "unit": "iter/sec",
            "range": "stddev: 0.000005391674952492769",
            "extra": "mean: 21.47759635867319 usec\nrounds: 15375"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 19898.06980819584,
            "unit": "iter/sec",
            "range": "stddev: 0.000018794047112558358",
            "extra": "mean: 50.25613085285834 usec\nrounds: 6878"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 62228.337029342336,
            "unit": "iter/sec",
            "range": "stddev: 0.000052406913878101963",
            "extra": "mean: 16.069849328103903 usec\nrounds: 24855"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 29651.47517765954,
            "unit": "iter/sec",
            "range": "stddev: 0.0000559258662906806",
            "extra": "mean: 33.725134888176996 usec\nrounds: 11024"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 40921.949534924905,
            "unit": "iter/sec",
            "range": "stddev: 0.00006038627905819555",
            "extra": "mean: 24.436763432948087 usec\nrounds: 8619"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 21943.685115728047,
            "unit": "iter/sec",
            "range": "stddev: 0.00011773244669037453",
            "extra": "mean: 45.571197122367295 usec\nrounds: 10359"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 8374.808326677748,
            "unit": "iter/sec",
            "range": "stddev: 0.00012375423978590094",
            "extra": "mean: 119.4057178376876 usec\nrounds: 5192"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 12702.267491653558,
            "unit": "iter/sec",
            "range": "stddev: 0.00012317717570293818",
            "extra": "mean: 78.72610151353551 usec\nrounds: 9595"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 8175.177985845038,
            "unit": "iter/sec",
            "range": "stddev: 0.00017765137721776242",
            "extra": "mean: 122.32149584161424 usec\nrounds: 6135"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 6162.094623082434,
            "unit": "iter/sec",
            "range": "stddev: 0.0001915081282697996",
            "extra": "mean: 162.28248041731223 usec\nrounds: 3064"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 3959.089290414121,
            "unit": "iter/sec",
            "range": "stddev: 0.0004283797366639667",
            "extra": "mean: 252.583340926721 usec\nrounds: 264"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 18808.40740750575,
            "unit": "iter/sec",
            "range": "stddev: 0.00023414561669845814",
            "extra": "mean: 53.16771262626608 usec\nrounds: 9726"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 15746.921223994303,
            "unit": "iter/sec",
            "range": "stddev: 0.0002828888051688183",
            "extra": "mean: 63.50447721020249 usec\nrounds: 10599"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 9875.70576408678,
            "unit": "iter/sec",
            "range": "stddev: 0.00021845204468135413",
            "extra": "mean: 101.25858585586073 usec\nrounds: 3832"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 4053.1690823481076,
            "unit": "iter/sec",
            "range": "stddev: 0.000498776237366152",
            "extra": "mean: 246.72052403515167 usec\nrounds: 2912"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 6863.278506048903,
            "unit": "iter/sec",
            "range": "stddev: 0.0002528504395417714",
            "extra": "mean: 145.7029609272969 usec\nrounds: 3455"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 5501.071214564902,
            "unit": "iter/sec",
            "range": "stddev: 0.00045245274969018834",
            "extra": "mean: 181.7827766621802 usec\nrounds: 5579"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 13035.487538218824,
            "unit": "iter/sec",
            "range": "stddev: 0.00029687860968158466",
            "extra": "mean: 76.71366314977435 usec\nrounds: 8630"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 8468.308227364205,
            "unit": "iter/sec",
            "range": "stddev: 0.0003430162392428574",
            "extra": "mean: 118.0873408420154 usec\nrounds: 1420"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 13049.995531512826,
            "unit": "iter/sec",
            "range": "stddev: 0.00021879471257787658",
            "extra": "mean: 76.62837872895996 usec\nrounds: 8378"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 8713.65874558889,
            "unit": "iter/sec",
            "range": "stddev: 0.0002019654087531381",
            "extra": "mean: 114.76235519393383 usec\nrounds: 2897"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 8807.802750063549,
            "unit": "iter/sec",
            "range": "stddev: 0.0002072860508922831",
            "extra": "mean: 113.53569424483138 usec\nrounds: 7264"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 49987.29241328792,
            "unit": "iter/sec",
            "range": "stddev: 0.00008046306041005862",
            "extra": "mean: 20.005084326875327 usec\nrounds: 14420"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 44986.60332343394,
            "unit": "iter/sec",
            "range": "stddev: 0.00009490507320643205",
            "extra": "mean: 22.2288398350602 usec\nrounds: 20629"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 64865.03611100583,
            "unit": "iter/sec",
            "range": "stddev: 0.00004676036674006428",
            "extra": "mean: 15.416625966085405 usec\nrounds: 16830"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 75096.62478442083,
            "unit": "iter/sec",
            "range": "stddev: 0.000054381284919537514",
            "extra": "mean: 13.316177696010847 usec\nrounds: 14823"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 65630.99868110887,
            "unit": "iter/sec",
            "range": "stddev: 0.00003350230485785908",
            "extra": "mean: 15.236702474372654 usec\nrounds: 19400"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 74002.34250594121,
            "unit": "iter/sec",
            "range": "stddev: 0.0000543181510794705",
            "extra": "mean: 13.513085750220894 usec\nrounds: 31067"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 94313.13527104094,
            "unit": "iter/sec",
            "range": "stddev: 0.000060857349615040054",
            "extra": "mean: 10.602976956774462 usec\nrounds: 32808"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 49631.867950432985,
            "unit": "iter/sec",
            "range": "stddev: 0.00003880026338011563",
            "extra": "mean: 20.148345031033156 usec\nrounds: 15845"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 62403.23375003672,
            "unit": "iter/sec",
            "range": "stddev: 0.00007303907035052989",
            "extra": "mean: 16.02481057320866 usec\nrounds: 26010"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 37930.33961695282,
            "unit": "iter/sec",
            "range": "stddev: 0.000050119851254944076",
            "extra": "mean: 26.364119332932464 usec\nrounds: 10785"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 21213.55151833162,
            "unit": "iter/sec",
            "range": "stddev: 0.000031489176163363624",
            "extra": "mean: 47.13967857460611 usec\nrounds: 308"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 159166.28296982622,
            "unit": "iter/sec",
            "range": "stddev: 0.00003248819907868572",
            "extra": "mean: 6.282737658638255 usec\nrounds: 37821"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 142356.77556682884,
            "unit": "iter/sec",
            "range": "stddev: 0.00001798894691382754",
            "extra": "mean: 7.02460417509635 usec\nrounds: 39126"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 158248.72674903017,
            "unit": "iter/sec",
            "range": "stddev: 0.000030368984568870153",
            "extra": "mean: 6.319166166726384 usec\nrounds: 41849"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 109563.97526095659,
            "unit": "iter/sec",
            "range": "stddev: 0.00003865399282739594",
            "extra": "mean: 9.12708759989975 usec\nrounds: 36917"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 191566.75261533336,
            "unit": "iter/sec",
            "range": "stddev: 0.000003867807646060812",
            "extra": "mean: 5.220112500460887 usec\nrounds: 8409"
          }
        ]
      },
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
          "id": "663bf67cf3a3493501ae6338421bfad97dc11ee6",
          "message": "Merge pull request #56 from amsdal/fix/dependencies\n\nFix dependencies",
          "timestamp": "2024-08-05T14:59:09+03:00",
          "tree_id": "36944311e3069bcbb2719ff549f4928080042170",
          "url": "https://github.com/amsdal/amsdal-glue/commit/663bf67cf3a3493501ae6338421bfad97dc11ee6"
        },
        "date": 1722868497465,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 42020.82153512798,
            "unit": "iter/sec",
            "range": "stddev: 0.000004738272778555214",
            "extra": "mean: 23.797726066922177 usec\nrounds: 3709"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 44327.40339444384,
            "unit": "iter/sec",
            "range": "stddev: 0.000006904052876531361",
            "extra": "mean: 22.5594084792556 usec\nrounds: 7878"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 71416.86253969451,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032731130240653307",
            "extra": "mean: 14.002295318478682 usec\nrounds: 16108"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 46878.45885227306,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026852920831273786",
            "extra": "mean: 21.33175928737921 usec\nrounds: 10660"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 132235.02245537765,
            "unit": "iter/sec",
            "range": "stddev: 0.00000156241160299903",
            "extra": "mean: 7.562293115936418 usec\nrounds: 27194"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 61394.4984864655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030603560759632086",
            "extra": "mean: 16.28810438480007 usec\nrounds: 11017"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 81481.2741196795,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017469513798289662",
            "extra": "mean: 12.272758505607097 usec\nrounds: 12493"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 52601.11648530368,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022953382609866525",
            "extra": "mean: 19.01100331738 usec\nrounds: 11152"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16691.27375630028,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047728831799210515",
            "extra": "mean: 59.911545074415926 usec\nrounds: 5935"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 32786.94285571804,
            "unit": "iter/sec",
            "range": "stddev: 0.000003512675746700007",
            "extra": "mean: 30.499946408562455 usec\nrounds: 10655"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 19994.990344389877,
            "unit": "iter/sec",
            "range": "stddev: 0.000013567319468265009",
            "extra": "mean: 50.012527276892456 usec\nrounds: 8157"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 13970.80594319678,
            "unit": "iter/sec",
            "range": "stddev: 0.000005551214296032864",
            "extra": "mean: 71.57783194941304 usec\nrounds: 6748"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 10933.867303941603,
            "unit": "iter/sec",
            "range": "stddev: 0.000006154319508361532",
            "extra": "mean: 91.45894789115513 usec\nrounds: 5719"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 67122.79623204983,
            "unit": "iter/sec",
            "range": "stddev: 0.00000192590814500786",
            "extra": "mean: 14.898068258999606 usec\nrounds: 15954"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 59852.07986300664,
            "unit": "iter/sec",
            "range": "stddev: 0.000002297496931852968",
            "extra": "mean: 16.707857141955056 usec\nrounds: 15715"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 27527.572090275316,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037460511242430203",
            "extra": "mean: 36.327213919213406 usec\nrounds: 7026"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 13961.923051703909,
            "unit": "iter/sec",
            "range": "stddev: 0.0000055210994742163085",
            "extra": "mean: 71.62337138636217 usec\nrounds: 4774"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 16618.82443466405,
            "unit": "iter/sec",
            "range": "stddev: 0.000005263485964988183",
            "extra": "mean: 60.17272785638012 usec\nrounds: 6390"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 19753.22830616037,
            "unit": "iter/sec",
            "range": "stddev: 0.000004733109399194381",
            "extra": "mean: 50.62463636326897 usec\nrounds: 6611"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 54904.39152094943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020937867217189054",
            "extra": "mean: 18.213479328305425 usec\nrounds: 16932"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 36371.64185658007,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027066835995596505",
            "extra": "mean: 27.493947178496366 usec\nrounds: 8652"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 40535.11415657163,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025063562051733937",
            "extra": "mean: 24.669968761834067 usec\nrounds: 12420"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 23329.295783434518,
            "unit": "iter/sec",
            "range": "stddev: 0.000004245592919582817",
            "extra": "mean: 42.86456004857515 usec\nrounds: 6503"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 21297.42712429244,
            "unit": "iter/sec",
            "range": "stddev: 0.000004649696922476682",
            "extra": "mean: 46.954028491984936 usec\nrounds: 8002"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 103135.60554441494,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014260985327765092",
            "extra": "mean: 9.695972547224283 usec\nrounds: 18942"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 84684.52502206349,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014929678932516211",
            "extra": "mean: 11.808532901843193 usec\nrounds: 25834"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 104943.16515559243,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013722941216742695",
            "extra": "mean: 9.52896740361666 usec\nrounds: 13959"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 131007.36052384181,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011993196609444039",
            "extra": "mean: 7.633158900396377 usec\nrounds: 33027"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 118571.88191570861,
            "unit": "iter/sec",
            "range": "stddev: 0.000001301704074047228",
            "extra": "mean: 8.43370269446249 usec\nrounds: 29135"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 132389.7776235697,
            "unit": "iter/sec",
            "range": "stddev: 0.000001256026929280158",
            "extra": "mean: 7.553453279779265 usec\nrounds: 31753"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 184117.87325744686,
            "unit": "iter/sec",
            "range": "stddev: 9.165307648976486e-7",
            "extra": "mean: 5.431303231499573 usec\nrounds: 32213"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 93238.92456824475,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014484173547052905",
            "extra": "mean: 10.725134428894725 usec\nrounds: 16678"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 125192.63243433801,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011800453265321377",
            "extra": "mean: 7.987690493883398 usec\nrounds: 29896"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 78399.87563200154,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018345541165230498",
            "extra": "mean: 12.75512227460494 usec\nrounds: 13167"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 43762.95543212633,
            "unit": "iter/sec",
            "range": "stddev: 0.000004183197877496492",
            "extra": "mean: 22.850376308586814 usec\nrounds: 287"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 279015.9386192182,
            "unit": "iter/sec",
            "range": "stddev: 7.155148550036959e-7",
            "extra": "mean: 3.5840246437130294 usec\nrounds: 50317"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 244863.6267037356,
            "unit": "iter/sec",
            "range": "stddev: 8.194040380873005e-7",
            "extra": "mean: 4.083905860015363 usec\nrounds: 46962"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 287711.1030230547,
            "unit": "iter/sec",
            "range": "stddev: 7.251565344165615e-7",
            "extra": "mean: 3.4757087560846354 usec\nrounds: 48207"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 194007.22765804915,
            "unit": "iter/sec",
            "range": "stddev: 9.175953237088589e-7",
            "extra": "mean: 5.154447141333144 usec\nrounds: 42519"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 292851.538909894,
            "unit": "iter/sec",
            "range": "stddev: 6.66216309299537e-7",
            "extra": "mean: 3.4146994880832255 usec\nrounds: 59312"
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
          "id": "6406b4ba318d6c5798798fe38eec6f1a9e0460db",
          "message": "Merge pull request #57 from amsdal/fixes/autocommit-true-for-pg\n\nFixes/autocommit true for pg",
          "timestamp": "2024-08-06T16:18:55+03:00",
          "tree_id": "4e8c82b5c0f5093fc1ca25f3a80e48a0431999e0",
          "url": "https://github.com/amsdal/amsdal-glue/commit/6406b4ba318d6c5798798fe38eec6f1a9e0460db"
        },
        "date": 1722950363073,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75023.37962369781,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021321795204507646",
            "extra": "mean: 13.329178251043862 usec\nrounds: 5352"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 52726.34869015471,
            "unit": "iter/sec",
            "range": "stddev: 0.000005441341118185615",
            "extra": "mean: 18.965849614895188 usec\nrounds: 12069"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 82722.51799742183,
            "unit": "iter/sec",
            "range": "stddev: 0.000002134796700393534",
            "extra": "mean: 12.088606877648072 usec\nrounds: 15354"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 51683.77403726477,
            "unit": "iter/sec",
            "range": "stddev: 0.000002388468613453112",
            "extra": "mean: 19.348432242563888 usec\nrounds: 10818"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 152667.36122466568,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010691075449246088",
            "extra": "mean: 6.550188540485725 usec\nrounds: 25289"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68500.68494450861,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019054712766246815",
            "extra": "mean: 14.598394173869723 usec\nrounds: 11500"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 88638.19218754474,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017031421020792648",
            "extra": "mean: 11.28181854029868 usec\nrounds: 10140"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 50305.11899327686,
            "unit": "iter/sec",
            "range": "stddev: 0.000005705918944673115",
            "extra": "mean: 19.87869266612106 usec\nrounds: 5577"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17899.04860248706,
            "unit": "iter/sec",
            "range": "stddev: 0.000007986660602183573",
            "extra": "mean: 55.868891258334855 usec\nrounds: 6704"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35258.852003319924,
            "unit": "iter/sec",
            "range": "stddev: 0.000003291343771593773",
            "extra": "mean: 28.36167212437437 usec\nrounds: 10077"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21743.4157767095,
            "unit": "iter/sec",
            "range": "stddev: 0.000014056804249352657",
            "extra": "mean: 45.99093400362384 usec\nrounds: 7955"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15402.114078558534,
            "unit": "iter/sec",
            "range": "stddev: 0.000005922652993654128",
            "extra": "mean: 64.92615201390515 usec\nrounds: 6802"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12170.801989591637,
            "unit": "iter/sec",
            "range": "stddev: 0.000006669829304225585",
            "extra": "mean: 82.16385418604223 usec\nrounds: 6570"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73198.6893928048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018319341065870225",
            "extra": "mean: 13.661446786754858 usec\nrounds: 16744"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65209.90906474096,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019155217376668844",
            "extra": "mean: 15.335092692848125 usec\nrounds: 16614"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30294.06305492741,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035642493980862275",
            "extra": "mean: 33.00976822378889 usec\nrounds: 8327"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15314.96161901808,
            "unit": "iter/sec",
            "range": "stddev: 0.000005821136508636266",
            "extra": "mean: 65.29562560301832 usec\nrounds: 5804"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18119.8849425174,
            "unit": "iter/sec",
            "range": "stddev: 0.00000688870855848777",
            "extra": "mean: 55.187988399062625 usec\nrounds: 6896"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21493.933324774953,
            "unit": "iter/sec",
            "range": "stddev: 0.000004808698330770841",
            "extra": "mean: 46.524755841098255 usec\nrounds: 6377"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 59103.184896227074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019449734057246917",
            "extra": "mean: 16.919561978864465 usec\nrounds: 17748"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 39955.966348929534,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045874091386327465",
            "extra": "mean: 25.027551361595116 usec\nrounds: 8664"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44805.81192126827,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023286584160116596",
            "extra": "mean: 22.31853317951646 usec\nrounds: 13442"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25709.96903832734,
            "unit": "iter/sec",
            "range": "stddev: 0.000004450697274749571",
            "extra": "mean: 38.89541829121778 usec\nrounds: 5642"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23542.479444293356,
            "unit": "iter/sec",
            "range": "stddev: 0.00000448799991688677",
            "extra": "mean: 42.476409605293206 usec\nrounds: 8225"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 114142.6653468935,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011970890848298851",
            "extra": "mean: 8.76096591016933 usec\nrounds: 19126"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 93964.96572629562,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014126912523234125",
            "extra": "mean: 10.64226429787496 usec\nrounds: 24514"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 116546.15076620854,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012666090467666655",
            "extra": "mean: 8.580291956668729 usec\nrounds: 17369"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 142314.6007219483,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010156289571790513",
            "extra": "mean: 7.026685912247204 usec\nrounds: 33376"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 130581.87271036183,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010614575048710429",
            "extra": "mean: 7.65803077597193 usec\nrounds: 20178"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 146645.02965260096,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011016845146977859",
            "extra": "mean: 6.81918781951887 usec\nrounds: 33266"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 202951.16426031245,
            "unit": "iter/sec",
            "range": "stddev: 8.564759548941736e-7",
            "extra": "mean: 4.927293734158451 usec\nrounds: 32829"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103119.41749583372,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012689301053693778",
            "extra": "mean: 9.69749465507214 usec\nrounds: 14032"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137722.8183388497,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010510890927593494",
            "extra": "mean: 7.260960907288621 usec\nrounds: 30031"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86822.96914952471,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014404407282620738",
            "extra": "mean: 11.517689498476155 usec\nrounds: 13198"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48602.89772402829,
            "unit": "iter/sec",
            "range": "stddev: 0.000004783197546936136",
            "extra": "mean: 20.574904930115313 usec\nrounds: 284"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 311972.41237576265,
            "unit": "iter/sec",
            "range": "stddev: 6.158455403952316e-7",
            "extra": "mean: 3.2054116336271616 usec\nrounds: 50698"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 268679.99386936217,
            "unit": "iter/sec",
            "range": "stddev: 6.926638536654654e-7",
            "extra": "mean: 3.7218997425101215 usec\nrounds: 43518"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324285.85243821534,
            "unit": "iter/sec",
            "range": "stddev: 6.13525953456858e-7",
            "extra": "mean: 3.0836991268082694 usec\nrounds: 43972"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 211400.06481560555,
            "unit": "iter/sec",
            "range": "stddev: 8.610515153006185e-7",
            "extra": "mean: 4.730367518440704 usec\nrounds: 48452"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 325913.4592606134,
            "unit": "iter/sec",
            "range": "stddev: 6.285020163886332e-7",
            "extra": "mean: 3.0682991806127284 usec\nrounds: 59917"
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
          "id": "a276bff4b144333523f6ea01ae74f4d7cb88e12e",
          "message": "Merge pull request #58 from amsdal/release/06-08-2024\n\nRelease/06 08 2024",
          "timestamp": "2024-08-06T16:38:54+03:00",
          "tree_id": "0ce73eab7889589f7b007e83aa3d4b8ca4f78692",
          "url": "https://github.com/amsdal/amsdal-glue/commit/a276bff4b144333523f6ea01ae74f4d7cb88e12e"
        },
        "date": 1722951583744,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75162.1894918355,
            "unit": "iter/sec",
            "range": "stddev: 0.000002002121841481935",
            "extra": "mean: 13.304561864960375 usec\nrounds: 5035"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 53778.91673355443,
            "unit": "iter/sec",
            "range": "stddev: 0.000005035567201912767",
            "extra": "mean: 18.59464750758111 usec\nrounds: 13745"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 84509.8260410714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017993592822234439",
            "extra": "mean: 11.832943538589282 usec\nrounds: 12983"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 48000.14657843392,
            "unit": "iter/sec",
            "range": "stddev: 0.000005100398070476161",
            "extra": "mean: 20.83326971441566 usec\nrounds: 10133"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 153015.4990781843,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013020039610731718",
            "extra": "mean: 6.535285680367863 usec\nrounds: 21195"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 69391.46073427628,
            "unit": "iter/sec",
            "range": "stddev: 0.000001945270280868782",
            "extra": "mean: 14.410995091014776 usec\nrounds: 11001"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 86745.9314605414,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025257390212413208",
            "extra": "mean: 11.527918176253323 usec\nrounds: 9386"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57804.70914449175,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021913658307957136",
            "extra": "mean: 17.299628608118176 usec\nrounds: 11018"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18271.14391183465,
            "unit": "iter/sec",
            "range": "stddev: 0.000005374993726907844",
            "extra": "mean: 54.73111069703065 usec\nrounds: 6450"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 33863.29297559287,
            "unit": "iter/sec",
            "range": "stddev: 0.000006421494096716936",
            "extra": "mean: 29.53050079095246 usec\nrounds: 10120"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21647.641965756775,
            "unit": "iter/sec",
            "range": "stddev: 0.000014559519539734876",
            "extra": "mean: 46.194407759600125 usec\nrounds: 7784"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15434.973061103135,
            "unit": "iter/sec",
            "range": "stddev: 0.000006471789864528217",
            "extra": "mean: 64.78793296504335 usec\nrounds: 7056"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12048.469956392742,
            "unit": "iter/sec",
            "range": "stddev: 0.000007160790084235911",
            "extra": "mean: 82.99809051434076 usec\nrounds: 6474"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73639.8135414045,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018946692233603842",
            "extra": "mean: 13.57961070118331 usec\nrounds: 15831"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 64695.91854480971,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023070834224660957",
            "extra": "mean: 15.45692560663436 usec\nrounds: 15808"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30560.16338602107,
            "unit": "iter/sec",
            "range": "stddev: 0.000003914410245568817",
            "extra": "mean: 32.7223381422569 usec\nrounds: 7973"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15378.717999181279,
            "unit": "iter/sec",
            "range": "stddev: 0.000006329244562332829",
            "extra": "mean: 65.02492600834721 usec\nrounds: 5352"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18298.923474984873,
            "unit": "iter/sec",
            "range": "stddev: 0.000006141593319608058",
            "extra": "mean: 54.648023495318036 usec\nrounds: 7108"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21439.296284758268,
            "unit": "iter/sec",
            "range": "stddev: 0.000005275983275388688",
            "extra": "mean: 46.64332199704358 usec\nrounds: 6910"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 59672.45609489419,
            "unit": "iter/sec",
            "range": "stddev: 0.000002100168216381264",
            "extra": "mean: 16.758150500957242 usec\nrounds: 16671"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40138.86381121437,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026613192376493452",
            "extra": "mean: 24.913510374965092 usec\nrounds: 7373"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44533.35158823821,
            "unit": "iter/sec",
            "range": "stddev: 0.000004353778057585865",
            "extra": "mean: 22.45508061567304 usec\nrounds: 6190"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25972.452281581707,
            "unit": "iter/sec",
            "range": "stddev: 0.000004685541150246652",
            "extra": "mean: 38.50233274696002 usec\nrounds: 5692"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23399.78657620445,
            "unit": "iter/sec",
            "range": "stddev: 0.000004801049814255311",
            "extra": "mean: 42.73543251103465 usec\nrounds: 6527"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115497.87407277273,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012680476255973988",
            "extra": "mean: 8.658168022815047 usec\nrounds: 19426"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95340.49462722994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015885725477971257",
            "extra": "mean: 10.488722592743846 usec\nrounds: 22887"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 118531.13348813119,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012706355739410798",
            "extra": "mean: 8.436602018153588 usec\nrounds: 16850"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 145291.80136146396,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010633863600774156",
            "extra": "mean: 6.882700817454603 usec\nrounds: 30229"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 131398.19506203872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011543690369398727",
            "extra": "mean: 7.61045461490439 usec\nrounds: 28578"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 147635.5819932436,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010822582821470272",
            "extra": "mean: 6.77343487592147 usec\nrounds: 31110"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 203270.9973366161,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010178731728864737",
            "extra": "mean: 4.919540972901331 usec\nrounds: 33218"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102582.18465719573,
            "unit": "iter/sec",
            "range": "stddev: 0.000001770470536663516",
            "extra": "mean: 9.748281374019793 usec\nrounds: 17084"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137045.67698799973,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010971574243957541",
            "extra": "mean: 7.296837244180741 usec\nrounds: 28171"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87016.81244539829,
            "unit": "iter/sec",
            "range": "stddev: 0.000001555410331183094",
            "extra": "mean: 11.492032078599577 usec\nrounds: 13280"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49648.431415092644,
            "unit": "iter/sec",
            "range": "stddev: 0.000005838210296179199",
            "extra": "mean: 20.14162323960168 usec\nrounds: 284"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 312568.70281846565,
            "unit": "iter/sec",
            "range": "stddev: 7.41443758733592e-7",
            "extra": "mean: 3.1992966377724077 usec\nrounds: 49461"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 271659.3523654011,
            "unit": "iter/sec",
            "range": "stddev: 0.000003307892563995695",
            "extra": "mean: 3.681080703803376 usec\nrounds: 37049"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 323070.98596661934,
            "unit": "iter/sec",
            "range": "stddev: 6.561819201804478e-7",
            "extra": "mean: 3.0952949767619273 usec\nrounds: 45851"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 217948.47053694056,
            "unit": "iter/sec",
            "range": "stddev: 8.156324950477545e-7",
            "extra": "mean: 4.588240502612326 usec\nrounds: 43879"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331142.02244631713,
            "unit": "iter/sec",
            "range": "stddev: 6.307168162931631e-7",
            "extra": "mean: 3.0198523057040103 usec\nrounds: 51911"
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
          "id": "cb53aca768ccf249ef6a46275de91cf72a68a6f5",
          "message": "Merge pull request #60 from amsdal/feature/jupiter-notebook\n\nJupiter Notebook: AMSDAL Glue: Multiple Postgres Connections Example",
          "timestamp": "2024-08-07T18:05:47+03:00",
          "tree_id": "e80fba4b15da3d4294d93d2539bda776453a2233",
          "url": "https://github.com/amsdal/amsdal-glue/commit/cb53aca768ccf249ef6a46275de91cf72a68a6f5"
        },
        "date": 1723043170595,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 64316.62775652782,
            "unit": "iter/sec",
            "range": "stddev: 0.000006607090407155853",
            "extra": "mean: 15.54807885428205 usec\nrounds: 4685"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 56412.41961958208,
            "unit": "iter/sec",
            "range": "stddev: 0.000010164026217136197",
            "extra": "mean: 17.726592951401724 usec\nrounds: 11478"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 83395.3087895383,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025102922888280026",
            "extra": "mean: 11.991082166548043 usec\nrounds: 15331"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 42067.210514365506,
            "unit": "iter/sec",
            "range": "stddev: 0.000013541464370367752",
            "extra": "mean: 23.771483484946323 usec\nrounds: 5914"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 155328.44580957084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014075154309078587",
            "extra": "mean: 6.437970809454807 usec\nrounds: 26947"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 63390.674488583805,
            "unit": "iter/sec",
            "range": "stddev: 0.00000429254220573651",
            "extra": "mean: 15.775191036657807 usec\nrounds: 11529"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 86148.24378226958,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028058717564413043",
            "extra": "mean: 11.607897690025958 usec\nrounds: 11722"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58069.649131235376,
            "unit": "iter/sec",
            "range": "stddev: 0.000002961905797224367",
            "extra": "mean: 17.220699882998 usec\nrounds: 12223"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18602.315930979064,
            "unit": "iter/sec",
            "range": "stddev: 0.000005518197845192915",
            "extra": "mean: 53.75674747759047 usec\nrounds: 6405"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 32799.37638880349,
            "unit": "iter/sec",
            "range": "stddev: 0.000008035370387289698",
            "extra": "mean: 30.488384539572028 usec\nrounds: 9749"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21974.00494526654,
            "unit": "iter/sec",
            "range": "stddev: 0.000013802961780440746",
            "extra": "mean: 45.508317782344534 usec\nrounds: 8061"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15554.93803752367,
            "unit": "iter/sec",
            "range": "stddev: 0.0000063545307123270635",
            "extra": "mean: 64.2882663748109 usec\nrounds: 7478"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12216.838777405139,
            "unit": "iter/sec",
            "range": "stddev: 0.000007190975533734329",
            "extra": "mean: 81.85423563495699 usec\nrounds: 5591"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74568.00277063156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018461278991383028",
            "extra": "mean: 13.410577765854388 usec\nrounds: 16784"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65946.31221066829,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020922269031683782",
            "extra": "mean: 15.163850205989649 usec\nrounds: 13848"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30679.29559764161,
            "unit": "iter/sec",
            "range": "stddev: 0.000004048172749969929",
            "extra": "mean: 32.59527249631091 usec\nrounds: 8684"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15464.531562130183,
            "unit": "iter/sec",
            "range": "stddev: 0.000006027802770455353",
            "extra": "mean: 64.66409900503017 usec\nrounds: 4658"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18309.61562430819,
            "unit": "iter/sec",
            "range": "stddev: 0.000005722027761034246",
            "extra": "mean: 54.61611103798275 usec\nrounds: 6879"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21984.785719936328,
            "unit": "iter/sec",
            "range": "stddev: 0.000005035417906585691",
            "extra": "mean: 45.48600167129107 usec\nrounds: 6856"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 61080.40095375624,
            "unit": "iter/sec",
            "range": "stddev: 0.000002254679212353111",
            "extra": "mean: 16.37186371381381 usec\nrounds: 14146"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40551.59301463215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030626609194317748",
            "extra": "mean: 24.659943683079774 usec\nrounds: 7477"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 43436.2672436351,
            "unit": "iter/sec",
            "range": "stddev: 0.000004192699491092206",
            "extra": "mean: 23.022236104934507 usec\nrounds: 11724"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25757.807772883953,
            "unit": "iter/sec",
            "range": "stddev: 0.000005002895391703903",
            "extra": "mean: 38.82317970602806 usec\nrounds: 5173"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23533.861381752737,
            "unit": "iter/sec",
            "range": "stddev: 0.0000048477086425332",
            "extra": "mean: 42.49196439881141 usec\nrounds: 7775"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 116779.9589249776,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012180363132599774",
            "extra": "mean: 8.563113133499433 usec\nrounds: 19016"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95950.05647539656,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015111313401293188",
            "extra": "mean: 10.422088706705653 usec\nrounds: 24205"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119820.73090631039,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012102345167395397",
            "extra": "mean: 8.345801201813023 usec\nrounds: 17972"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 145039.5605044629,
            "unit": "iter/sec",
            "range": "stddev: 0.000001028496631393962",
            "extra": "mean: 6.894670643801557 usec\nrounds: 29627"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132941.68624414288,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010566030182479544",
            "extra": "mean: 7.522095049731309 usec\nrounds: 29981"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 150675.06372692756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010554304186055217",
            "extra": "mean: 6.6367982549012 usec\nrounds: 31532"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 206382.66700420686,
            "unit": "iter/sec",
            "range": "stddev: 9.128743527258104e-7",
            "extra": "mean: 4.845368143147487 usec\nrounds: 34592"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104290.68960391592,
            "unit": "iter/sec",
            "range": "stddev: 0.000001338603556807298",
            "extra": "mean: 9.588583638653512 usec\nrounds: 17209"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138399.2442096103,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010653464091714853",
            "extra": "mean: 7.2254729836925 usec\nrounds: 27546"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88617.04461785291,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015497939157085812",
            "extra": "mean: 11.284510833241427 usec\nrounds: 12959"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50601.626638119415,
            "unit": "iter/sec",
            "range": "stddev: 0.000003921309579043571",
            "extra": "mean: 19.762210554051165 usec\nrounds: 285"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 320449.3570825204,
            "unit": "iter/sec",
            "range": "stddev: 7.3303705424725e-7",
            "extra": "mean: 3.1206179007639117 usec\nrounds: 51441"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 277264.3358097667,
            "unit": "iter/sec",
            "range": "stddev: 7.110840064324803e-7",
            "extra": "mean: 3.606666530260524 usec\nrounds: 47706"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324576.4787472293,
            "unit": "iter/sec",
            "range": "stddev: 6.166150958987271e-7",
            "extra": "mean: 3.080937977575297 usec\nrounds: 43249"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 218447.89899658752,
            "unit": "iter/sec",
            "range": "stddev: 8.027593828486377e-7",
            "extra": "mean: 4.577750596793891 usec\nrounds: 42801"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331052.29395954765,
            "unit": "iter/sec",
            "range": "stddev: 5.936140122669077e-7",
            "extra": "mean: 3.020670807138987 usec\nrounds: 30565"
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
          "id": "25de1eab8ddce39ff96fdff9489e87897f77d4a7",
          "message": "Merge pull request #61 from amsdal/feature/jupiter-notebook\n\nJupiter Notebook: AMSDAL Glue: Multiple Postgres Connections Example …",
          "timestamp": "2024-08-07T18:10:47+03:00",
          "tree_id": "3cb35079b81b4345fb60a730130b7dee5def9f11",
          "url": "https://github.com/amsdal/amsdal-glue/commit/25de1eab8ddce39ff96fdff9489e87897f77d4a7"
        },
        "date": 1723043495586,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 47501.19077774071,
            "unit": "iter/sec",
            "range": "stddev: 0.000005116633019943065",
            "extra": "mean: 21.052103823649933 usec\nrounds: 3630"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 45782.26051935622,
            "unit": "iter/sec",
            "range": "stddev: 0.000006874679592069102",
            "extra": "mean: 21.84252128785147 usec\nrounds: 10240"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 81214.9764123501,
            "unit": "iter/sec",
            "range": "stddev: 0.00000304700906919757",
            "extra": "mean: 12.312999943787872 usec\nrounds: 16000"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 52264.72451903003,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027971914352628784",
            "extra": "mean: 19.133364027124863 usec\nrounds: 10040"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 155011.59760144836,
            "unit": "iter/sec",
            "range": "stddev: 0.000001216199881274629",
            "extra": "mean: 6.451130208793206 usec\nrounds: 25494"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 70787.93746284622,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022240862746686592",
            "extra": "mean: 14.126700619365556 usec\nrounds: 11541"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 86620.84047672599,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026630196078478544",
            "extra": "mean: 11.544565886181724 usec\nrounds: 9090"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58226.0507358029,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023151662163492666",
            "extra": "mean: 17.174443180724005 usec\nrounds: 10263"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18679.383603455637,
            "unit": "iter/sec",
            "range": "stddev: 0.000005474511953997304",
            "extra": "mean: 53.53495710720361 usec\nrounds: 6447"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36220.94805184228,
            "unit": "iter/sec",
            "range": "stddev: 0.000004138264236136598",
            "extra": "mean: 27.60833312724783 usec\nrounds: 10235"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 20952.39602370596,
            "unit": "iter/sec",
            "range": "stddev: 0.000018377271858384034",
            "extra": "mean: 47.72723839643829 usec\nrounds: 6667"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15608.183011676001,
            "unit": "iter/sec",
            "range": "stddev: 0.000006579462543716348",
            "extra": "mean: 64.06895660128606 usec\nrounds: 5421"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12213.771799089936,
            "unit": "iter/sec",
            "range": "stddev: 0.0000074984552817030875",
            "extra": "mean: 81.87478990515535 usec\nrounds: 6307"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74671.96675677612,
            "unit": "iter/sec",
            "range": "stddev: 0.000001931955462990389",
            "extra": "mean: 13.391906540472295 usec\nrounds: 15002"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 67156.29129838014,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020572397011076302",
            "extra": "mean: 14.890637655330451 usec\nrounds: 16779"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30885.94518205824,
            "unit": "iter/sec",
            "range": "stddev: 0.000004267072569061887",
            "extra": "mean: 32.377186260788406 usec\nrounds: 7090"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15434.82930194816,
            "unit": "iter/sec",
            "range": "stddev: 0.0000067716199014218755",
            "extra": "mean: 64.78853639630348 usec\nrounds: 5187"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18417.79010339127,
            "unit": "iter/sec",
            "range": "stddev: 0.000005795041557052737",
            "extra": "mean: 54.295330459644546 usec\nrounds: 7165"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21911.11798173334,
            "unit": "iter/sec",
            "range": "stddev: 0.000005157617121161868",
            "extra": "mean: 45.63893092235964 usec\nrounds: 6169"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 59877.59770607452,
            "unit": "iter/sec",
            "range": "stddev: 0.000002112501728314025",
            "extra": "mean: 16.70073680825961 usec\nrounds: 16959"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40534.03529922586,
            "unit": "iter/sec",
            "range": "stddev: 0.000006804127604719327",
            "extra": "mean: 24.670625379829836 usec\nrounds: 8643"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45493.55764241825,
            "unit": "iter/sec",
            "range": "stddev: 0.000002773513797737157",
            "extra": "mean: 21.981134292904773 usec\nrounds: 9706"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26758.445359676163,
            "unit": "iter/sec",
            "range": "stddev: 0.000004722706851718603",
            "extra": "mean: 37.37137888836238 usec\nrounds: 6537"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24041.07898791025,
            "unit": "iter/sec",
            "range": "stddev: 0.000004891892851012721",
            "extra": "mean: 41.595470839843706 usec\nrounds: 8281"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117040.09870961911,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012449336767092977",
            "extra": "mean: 8.544080285518536 usec\nrounds: 19416"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96663.06823183947,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014744904918727607",
            "extra": "mean: 10.345212688692763 usec\nrounds: 22680"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 121101.0734385067,
            "unit": "iter/sec",
            "range": "stddev: 0.000001178769716637409",
            "extra": "mean: 8.257565119831781 usec\nrounds: 14054"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 148536.25995512068,
            "unit": "iter/sec",
            "range": "stddev: 9.846672316882764e-7",
            "extra": "mean: 6.732362860773147 usec\nrounds: 30493"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 133731.32952509308,
            "unit": "iter/sec",
            "range": "stddev: 0.000001111881053995564",
            "extra": "mean: 7.477679340743875 usec\nrounds: 29107"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148842.41378917036,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010180280070935875",
            "extra": "mean: 6.718515069343487 usec\nrounds: 34083"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 210906.63747500628,
            "unit": "iter/sec",
            "range": "stddev: 8.490630931147861e-7",
            "extra": "mean: 4.741434465847505 usec\nrounds: 35196"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 106102.49391030244,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012988067903452894",
            "extra": "mean: 9.424849154303443 usec\nrounds: 17186"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 140770.8909310011,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010787825960287815",
            "extra": "mean: 7.103741358646017 usec\nrounds: 27941"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87607.85145159219,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015525758604205998",
            "extra": "mean: 11.414502050110785 usec\nrounds: 12615"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50138.73357885539,
            "unit": "iter/sec",
            "range": "stddev: 0.0000041011786328538365",
            "extra": "mean: 19.94466011845425 usec\nrounds: 285"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 315911.46811783395,
            "unit": "iter/sec",
            "range": "stddev: 6.377319734745852e-7",
            "extra": "mean: 3.1654438060064454 usec\nrounds: 49769"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 278053.94792294,
            "unit": "iter/sec",
            "range": "stddev: 7.42981393375671e-7",
            "extra": "mean: 3.596424389835099 usec\nrounds: 45113"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 322663.9933971812,
            "unit": "iter/sec",
            "range": "stddev: 6.181649062542234e-7",
            "extra": "mean: 3.0991992303555738 usec\nrounds: 44286"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 218347.7445812724,
            "unit": "iter/sec",
            "range": "stddev: 7.750091632109874e-7",
            "extra": "mean: 4.579850375453659 usec\nrounds: 40651"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 325583.9709632784,
            "unit": "iter/sec",
            "range": "stddev: 6.336576611809304e-7",
            "extra": "mean: 3.0714042741151624 usec\nrounds: 58789"
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
          "id": "be3a7e85e94a6ce30698920c51bcfe14e3076a56",
          "message": "Merge pull request #62 from amsdal/feature/jupiter-notebook\n\nJupiter Notebook: AMSDAL Glue: Multiple Postgres Connections Example …",
          "timestamp": "2024-08-08T11:37:28+03:00",
          "tree_id": "2028db4edbea9284396c2107205e5d7061e3d79e",
          "url": "https://github.com/amsdal/amsdal-glue/commit/be3a7e85e94a6ce30698920c51bcfe14e3076a56"
        },
        "date": 1723106299008,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 76488.78949256644,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018247694652751074",
            "extra": "mean: 13.073811294885047 usec\nrounds: 4780"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 60445.6554042985,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020488118150470903",
            "extra": "mean: 16.54378620450671 usec\nrounds: 15042"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 85219.04317589334,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015787389561194614",
            "extra": "mean: 11.734466414226048 usec\nrounds: 15683"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 45310.60825539367,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064776376177498385",
            "extra": "mean: 22.069886909561898 usec\nrounds: 10044"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 149905.0849937421,
            "unit": "iter/sec",
            "range": "stddev: 0.000001381324533337746",
            "extra": "mean: 6.67088778237073 usec\nrounds: 26608"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68000.56883557985,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021688765701457304",
            "extra": "mean: 14.705759335895014 usec\nrounds: 10974"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 86773.2335645328,
            "unit": "iter/sec",
            "range": "stddev: 0.000002420221813371222",
            "extra": "mean: 11.524291062131564 usec\nrounds: 9235"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58334.647982564515,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022604169882588365",
            "extra": "mean: 17.142470805667454 usec\nrounds: 11396"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18353.268111254205,
            "unit": "iter/sec",
            "range": "stddev: 0.000005260285718617738",
            "extra": "mean: 54.48620888324521 usec\nrounds: 5749"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36076.741161290636,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034894648379597693",
            "extra": "mean: 27.718689876373112 usec\nrounds: 10803"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21571.45313985574,
            "unit": "iter/sec",
            "range": "stddev: 0.000015303887186243397",
            "extra": "mean: 46.35756309584841 usec\nrounds: 8264"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15457.695606641902,
            "unit": "iter/sec",
            "range": "stddev: 0.000005835523845328996",
            "extra": "mean: 64.69269582267601 usec\nrounds: 5847"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12002.710177229015,
            "unit": "iter/sec",
            "range": "stddev: 0.00000721630188139124",
            "extra": "mean: 83.31451690778584 usec\nrounds: 5923"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74504.08306282417,
            "unit": "iter/sec",
            "range": "stddev: 0.000001735861047106178",
            "extra": "mean: 13.422083178404717 usec\nrounds: 15614"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65929.96266266685,
            "unit": "iter/sec",
            "range": "stddev: 0.000002007243080375839",
            "extra": "mean: 15.167610591811462 usec\nrounds: 16869"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30288.854179763006,
            "unit": "iter/sec",
            "range": "stddev: 0.000003555328718792334",
            "extra": "mean: 33.01544502360652 usec\nrounds: 8397"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15352.232055166054,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058525439164145455",
            "extra": "mean: 65.1371081681571 usec\nrounds: 5289"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18228.20297463306,
            "unit": "iter/sec",
            "range": "stddev: 0.000005953967100699306",
            "extra": "mean: 54.86004305479983 usec\nrounds: 6823"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21737.74539401033,
            "unit": "iter/sec",
            "range": "stddev: 0.000004706934395688207",
            "extra": "mean: 46.00293093300938 usec\nrounds: 7122"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 59796.035664182666,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019546323563469595",
            "extra": "mean: 16.723516682879225 usec\nrounds: 17853"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 39521.14642994956,
            "unit": "iter/sec",
            "range": "stddev: 0.000002844185756718186",
            "extra": "mean: 25.302909716257343 usec\nrounds: 5872"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44278.64129085672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026097090279553058",
            "extra": "mean: 22.584252155146736 usec\nrounds: 11884"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25325.131264475505,
            "unit": "iter/sec",
            "range": "stddev: 0.000004530498932213628",
            "extra": "mean: 39.486468581615476 usec\nrounds: 5572"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23300.327698307203,
            "unit": "iter/sec",
            "range": "stddev: 0.000004799980936718131",
            "extra": "mean: 42.91785132587003 usec\nrounds: 8672"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115115.85781566429,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015077124607355194",
            "extra": "mean: 8.686900475530539 usec\nrounds: 16744"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 94156.38778348258,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015697406467609452",
            "extra": "mean: 10.62062833484597 usec\nrounds: 25071"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 116804.74239040083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012002651258228844",
            "extra": "mean: 8.561296224237735 usec\nrounds: 17394"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 144873.48341707952,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010301447551072565",
            "extra": "mean: 6.902574414677926 usec\nrounds: 32076"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 131015.11378404903,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011620067758564149",
            "extra": "mean: 7.632707182533845 usec\nrounds: 27749"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 146587.41972460056,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011523906485305697",
            "extra": "mean: 6.821867810203211 usec\nrounds: 32564"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 199742.11753846554,
            "unit": "iter/sec",
            "range": "stddev: 8.205235940791561e-7",
            "extra": "mean: 5.006455385191479 usec\nrounds: 33585"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 100711.66899328423,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017799169384469322",
            "extra": "mean: 9.929335994488218 usec\nrounds: 16721"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137318.92706758264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010519705035911592",
            "extra": "mean: 7.282317313095826 usec\nrounds: 28822"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 85867.41184394143,
            "unit": "iter/sec",
            "range": "stddev: 0.000003213099126528987",
            "extra": "mean: 11.645861666559096 usec\nrounds: 13113"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48686.25898851857,
            "unit": "iter/sec",
            "range": "stddev: 0.000004190814094012282",
            "extra": "mean: 20.53967630242087 usec\nrounds: 281"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 316960.0799796321,
            "unit": "iter/sec",
            "range": "stddev: 7.229215431755635e-7",
            "extra": "mean: 3.1549714401392754 usec\nrounds: 48089"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 274337.0787473363,
            "unit": "iter/sec",
            "range": "stddev: 6.772049505186467e-7",
            "extra": "mean: 3.6451507195678694 usec\nrounds: 39279"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 321660.970050905,
            "unit": "iter/sec",
            "range": "stddev: 5.907725840906597e-7",
            "extra": "mean: 3.1088633471500855 usec\nrounds: 44246"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 216446.01158254532,
            "unit": "iter/sec",
            "range": "stddev: 7.680939012519883e-7",
            "extra": "mean: 4.620089752121087 usec\nrounds: 40775"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331584.2306183156,
            "unit": "iter/sec",
            "range": "stddev: 6.652542955167449e-7",
            "extra": "mean: 3.015824962891837 usec\nrounds: 54443"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "83cdaba6c3044c7557a1fd7a48167101ea67c302",
          "message": "Merge pull request #59 from amsdal/release-in-a-separate-branch\n\nadded script for release",
          "timestamp": "2024-08-09T13:04:41+03:00",
          "tree_id": "2351f3f15becf7c622388deb9195438ba7121478",
          "url": "https://github.com/amsdal/amsdal-glue/commit/83cdaba6c3044c7557a1fd7a48167101ea67c302"
        },
        "date": 1723197907453,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75872.4152926995,
            "unit": "iter/sec",
            "range": "stddev: 0.000002150511808972502",
            "extra": "mean: 13.180020645740807 usec\nrounds: 4028"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 51830.46622317656,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058228783201159875",
            "extra": "mean: 19.293671712195383 usec\nrounds: 12183"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 77075.9616537471,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035284017485526305",
            "extra": "mean: 12.97421373076549 usec\nrounds: 16329"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 50956.4456222277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036055707288708697",
            "extra": "mean: 19.624602693320316 usec\nrounds: 8967"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 153742.88890035046,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012340522850725695",
            "extra": "mean: 6.504365874431806 usec\nrounds: 16668"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 69625.51215873708,
            "unit": "iter/sec",
            "range": "stddev: 0.000001922253649028794",
            "extra": "mean: 14.362551441203484 usec\nrounds: 10747"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 91812.13514041527,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015531883702599942",
            "extra": "mean: 10.891806387800743 usec\nrounds: 11906"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57645.08693759348,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024502001679165643",
            "extra": "mean: 17.347532168397965 usec\nrounds: 11093"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18819.24263856497,
            "unit": "iter/sec",
            "range": "stddev: 0.00000524618576219745",
            "extra": "mean: 53.137101168501296 usec\nrounds: 6129"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36373.109028194616,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036427032326764826",
            "extra": "mean: 27.492838163073987 usec\nrounds: 9495"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21946.53830710722,
            "unit": "iter/sec",
            "range": "stddev: 0.000014157462354597676",
            "extra": "mean: 45.56527257313093 usec\nrounds: 7674"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15514.382154302662,
            "unit": "iter/sec",
            "range": "stddev: 0.000006248153325361851",
            "extra": "mean: 64.45632124142735 usec\nrounds: 7290"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12173.636248342318,
            "unit": "iter/sec",
            "range": "stddev: 0.000008417887064916338",
            "extra": "mean: 82.1447248463802 usec\nrounds: 5641"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74702.79722359573,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019660794406667124",
            "extra": "mean: 13.386379589064955 usec\nrounds: 17333"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65948.01850508718,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020588476955766037",
            "extra": "mean: 15.16345786678732 usec\nrounds: 18683"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30922.77611165898,
            "unit": "iter/sec",
            "range": "stddev: 0.000004098330553881989",
            "extra": "mean: 32.33862303918323 usec\nrounds: 7468"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15366.226837856175,
            "unit": "iter/sec",
            "range": "stddev: 0.000006137051514604616",
            "extra": "mean: 65.07778458251079 usec\nrounds: 5345"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18518.544191303085,
            "unit": "iter/sec",
            "range": "stddev: 0.000005465435945804251",
            "extra": "mean: 53.99992513826398 usec\nrounds: 7549"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22029.960330275902,
            "unit": "iter/sec",
            "range": "stddev: 0.000004969331116253015",
            "extra": "mean: 45.39272813059468 usec\nrounds: 6605"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 60756.086440001294,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020368768277298636",
            "extra": "mean: 16.459256324673483 usec\nrounds: 17258"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40164.3816129622,
            "unit": "iter/sec",
            "range": "stddev: 0.000002608204652358927",
            "extra": "mean: 24.89768197196073 usec\nrounds: 8441"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44816.638769986836,
            "unit": "iter/sec",
            "range": "stddev: 0.00000251339537964115",
            "extra": "mean: 22.313141445799097 usec\nrounds: 12423"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26154.145743783312,
            "unit": "iter/sec",
            "range": "stddev: 0.000004709549745842706",
            "extra": "mean: 38.2348561408355 usec\nrounds: 6474"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23643.336862728826,
            "unit": "iter/sec",
            "range": "stddev: 0.000004898754498661689",
            "extra": "mean: 42.29521432638352 usec\nrounds: 5894"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115554.8904991937,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012757779840543464",
            "extra": "mean: 8.6538959595741 usec\nrounds: 18360"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 94055.99000264068,
            "unit": "iter/sec",
            "range": "stddev: 0.000001413200008663325",
            "extra": "mean: 10.631965066466522 usec\nrounds: 23250"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 117367.59790006418,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012209375430487247",
            "extra": "mean: 8.520239128106525 usec\nrounds: 16078"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 145714.12295430788,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010567701481142564",
            "extra": "mean: 6.862752763598445 usec\nrounds: 17995"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 133809.2062032172,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010770194844084606",
            "extra": "mean: 7.473327347008481 usec\nrounds: 30878"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148380.7963800785,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010123914857883746",
            "extra": "mean: 6.739416584869195 usec\nrounds: 31967"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 206707.20267406548,
            "unit": "iter/sec",
            "range": "stddev: 9.343595035104973e-7",
            "extra": "mean: 4.837760789481503 usec\nrounds: 31726"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103324.8124579914,
            "unit": "iter/sec",
            "range": "stddev: 0.000001406527248429382",
            "extra": "mean: 9.67821742145981 usec\nrounds: 16405"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137918.59223321915,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010636093353507163",
            "extra": "mean: 7.250654054741282 usec\nrounds: 27641"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87668.8580615808,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015612440465072561",
            "extra": "mean: 11.406558977847926 usec\nrounds: 13429"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49849.77158396302,
            "unit": "iter/sec",
            "range": "stddev: 0.000004367386672567994",
            "extra": "mean: 20.060272459136126 usec\nrounds: 286"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 316229.5111738997,
            "unit": "iter/sec",
            "range": "stddev: 6.592351464520499e-7",
            "extra": "mean: 3.1622602086940703 usec\nrounds: 49476"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 273295.7393626524,
            "unit": "iter/sec",
            "range": "stddev: 6.88041212552235e-7",
            "extra": "mean: 3.6590398457439552 usec\nrounds: 46545"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324253.27484240767,
            "unit": "iter/sec",
            "range": "stddev: 7.462106157653061e-7",
            "extra": "mean: 3.084008944816413 usec\nrounds: 45297"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 218703.5429266562,
            "unit": "iter/sec",
            "range": "stddev: 8.379107729560556e-7",
            "extra": "mean: 4.572399635681061 usec\nrounds: 36057"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 327622.0605208171,
            "unit": "iter/sec",
            "range": "stddev: 6.618160809290846e-7",
            "extra": "mean: 3.0522975113773207 usec\nrounds: 47119"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b2117e36e2739809c609214d01a4457a783485a3",
          "message": "Merge pull request #63 from amsdal/fix-tag-push\n\nfix tag push",
          "timestamp": "2024-08-09T13:43:28+03:00",
          "tree_id": "682cc92007f273c858ba026084a49a843712b90c",
          "url": "https://github.com/amsdal/amsdal-glue/commit/b2117e36e2739809c609214d01a4457a783485a3"
        },
        "date": 1723200255696,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 77538.76648891093,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018528194508328122",
            "extra": "mean: 12.896774675194417 usec\nrounds: 4517"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59562.76747012612,
            "unit": "iter/sec",
            "range": "stddev: 0.000002573915771865252",
            "extra": "mean: 16.789011701001854 usec\nrounds: 16019"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 81096.76646321923,
            "unit": "iter/sec",
            "range": "stddev: 0.000002914663083703004",
            "extra": "mean: 12.330947873902492 usec\nrounds: 15990"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 50047.9709646752,
            "unit": "iter/sec",
            "range": "stddev: 0.0000041256895666498325",
            "extra": "mean: 19.980830006191837 usec\nrounds: 10625"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 155269.75912857297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011139953529337574",
            "extra": "mean: 6.440404143165689 usec\nrounds: 28734"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 69877.94694210883,
            "unit": "iter/sec",
            "range": "stddev: 0.000002042663647094791",
            "extra": "mean: 14.310666580236841 usec\nrounds: 9458"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 90138.13282711053,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017163101713446077",
            "extra": "mean: 11.09408380932463 usec\nrounds: 8913"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 56096.34584766618,
            "unit": "iter/sec",
            "range": "stddev: 0.000003686537496927449",
            "extra": "mean: 17.826473095334492 usec\nrounds: 11235"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18350.341710504494,
            "unit": "iter/sec",
            "range": "stddev: 0.00000637894603215877",
            "extra": "mean: 54.49489801203858 usec\nrounds: 6202"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35967.33478382822,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035079102898350706",
            "extra": "mean: 27.803005310519257 usec\nrounds: 11124"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21967.658141283355,
            "unit": "iter/sec",
            "range": "stddev: 0.000015280382909385947",
            "extra": "mean: 45.52146585533035 usec\nrounds: 7590"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15584.335139496463,
            "unit": "iter/sec",
            "range": "stddev: 0.000006181087749731981",
            "extra": "mean: 64.16699788915798 usec\nrounds: 7180"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12223.964016009615,
            "unit": "iter/sec",
            "range": "stddev: 0.000007006966160112329",
            "extra": "mean: 81.80652353772548 usec\nrounds: 6351"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74494.37364037767,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018289071934856723",
            "extra": "mean: 13.42383258133708 usec\nrounds: 16002"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66429.0273258578,
            "unit": "iter/sec",
            "range": "stddev: 0.000002001681417980688",
            "extra": "mean: 15.053660128043836 usec\nrounds: 15596"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 31030.800535225248,
            "unit": "iter/sec",
            "range": "stddev: 0.000003732190369609118",
            "extra": "mean: 32.226045823884874 usec\nrounds: 7952"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15552.87951351382,
            "unit": "iter/sec",
            "range": "stddev: 0.000005702091084072301",
            "extra": "mean: 64.29677534189761 usec\nrounds: 4516"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18498.113764391535,
            "unit": "iter/sec",
            "range": "stddev: 0.000005755857157047506",
            "extra": "mean: 54.05956589611737 usec\nrounds: 6942"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22000.46337315809,
            "unit": "iter/sec",
            "range": "stddev: 0.000005030237677780715",
            "extra": "mean: 45.453588092151776 usec\nrounds: 7177"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 60876.161726812985,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020259249672634933",
            "extra": "mean: 16.426791237062318 usec\nrounds: 16690"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40365.050299242714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026534104574322862",
            "extra": "mean: 24.77390694639518 usec\nrounds: 8494"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45542.91309964082,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024883739234089028",
            "extra": "mean: 21.957313046975173 usec\nrounds: 12770"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25992.894709607364,
            "unit": "iter/sec",
            "range": "stddev: 0.000004229213017080324",
            "extra": "mean: 38.47205211931955 usec\nrounds: 5819"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23917.731166892252,
            "unit": "iter/sec",
            "range": "stddev: 0.000004554098611984491",
            "extra": "mean: 41.80998578093538 usec\nrounds: 8395"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117404.99537261034,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011685327615939849",
            "extra": "mean: 8.517525142999938 usec\nrounds: 18747"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95269.13282136442,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015030491780413483",
            "extra": "mean: 10.496579221257976 usec\nrounds: 24694"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 120120.23756396396,
            "unit": "iter/sec",
            "range": "stddev: 0.000001186762600763888",
            "extra": "mean: 8.324991860488957 usec\nrounds: 16074"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 145161.24252343253,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010612956325444518",
            "extra": "mean: 6.8888911572837745 usec\nrounds: 31962"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132583.9106683129,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010795857280494243",
            "extra": "mean: 7.542393303677055 usec\nrounds: 27998"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 150821.17181003885,
            "unit": "iter/sec",
            "range": "stddev: 9.933202927096088e-7",
            "extra": "mean: 6.630368853382948 usec\nrounds: 31014"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 208308.343069032,
            "unit": "iter/sec",
            "range": "stddev: 9.695553267004756e-7",
            "extra": "mean: 4.800575844763965 usec\nrounds: 31556"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104486.28293866111,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012460568008521658",
            "extra": "mean: 9.570634267725382 usec\nrounds: 16216"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 139287.1773212427,
            "unit": "iter/sec",
            "range": "stddev: 0.000001014867766572154",
            "extra": "mean: 7.179411768060073 usec\nrounds: 30040"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86630.66223639458,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016703289344265303",
            "extra": "mean: 11.543257019913304 usec\nrounds: 13005"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50833.8079450844,
            "unit": "iter/sec",
            "range": "stddev: 0.000003797637766461319",
            "extra": "mean: 19.67194747795201 usec\nrounds: 286"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 316751.35336775327,
            "unit": "iter/sec",
            "range": "stddev: 6.982998298354478e-7",
            "extra": "mean: 3.1570504415145604 usec\nrounds: 52654"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 276173.83506194915,
            "unit": "iter/sec",
            "range": "stddev: 7.113712645453732e-7",
            "extra": "mean: 3.620907823421027 usec\nrounds: 45294"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 326046.3565678266,
            "unit": "iter/sec",
            "range": "stddev: 6.606816166213848e-7",
            "extra": "mean: 3.0670485342226868 usec\nrounds: 44453"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220176.3990996185,
            "unit": "iter/sec",
            "range": "stddev: 7.968585383983696e-7",
            "extra": "mean: 4.541812855916276 usec\nrounds: 44615"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 333921.43471796217,
            "unit": "iter/sec",
            "range": "stddev: 6.78541357046086e-7",
            "extra": "mean: 2.994716409399185 usec\nrounds: 58855"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "02ec8f33a519cbc2210266560577f28dbbe21484",
          "message": "Merge pull request #64 from amsdal/fix/ci-cd\n\nfix ci/cd",
          "timestamp": "2024-08-15T12:56:03+03:00",
          "tree_id": "c96cd04d70e901f7c1e1c6d7a59ab4c43f55caa1",
          "url": "https://github.com/amsdal/amsdal-glue/commit/02ec8f33a519cbc2210266560577f28dbbe21484"
        },
        "date": 1723715787937,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75957.3937195231,
            "unit": "iter/sec",
            "range": "stddev: 0.000002015229668020084",
            "extra": "mean: 13.165275308056986 usec\nrounds: 4548"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 56248.02856037414,
            "unit": "iter/sec",
            "range": "stddev: 0.000004160528131473231",
            "extra": "mean: 17.77840087189268 usec\nrounds: 16721"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 82342.16742065517,
            "unit": "iter/sec",
            "range": "stddev: 0.000002552041629704423",
            "extra": "mean: 12.144445930010273 usec\nrounds: 17345"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 48538.49982666077,
            "unit": "iter/sec",
            "range": "stddev: 0.000005393473982736351",
            "extra": "mean: 20.602202449007894 usec\nrounds: 7197"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 147046.64716567387,
            "unit": "iter/sec",
            "range": "stddev: 0.000001657177399095197",
            "extra": "mean: 6.800563081681994 usec\nrounds: 25820"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 69378.30896404557,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026656681976688086",
            "extra": "mean: 14.413726926066147 usec\nrounds: 11026"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 89257.94824006932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016453210415368556",
            "extra": "mean: 11.203484056236507 usec\nrounds: 11442"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58962.8142962076,
            "unit": "iter/sec",
            "range": "stddev: 0.00000199169035205569",
            "extra": "mean: 16.959841756812455 usec\nrounds: 10726"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18867.53838196389,
            "unit": "iter/sec",
            "range": "stddev: 0.000005357047683740992",
            "extra": "mean: 53.00108470726279 usec\nrounds: 6380"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36371.15065268562,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034616995216173567",
            "extra": "mean: 27.494318492949876 usec\nrounds: 11147"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21983.339892003256,
            "unit": "iter/sec",
            "range": "stddev: 0.000015640803244580092",
            "extra": "mean: 45.48899325182903 usec\nrounds: 6971"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15642.253607320468,
            "unit": "iter/sec",
            "range": "stddev: 0.000005897521307430069",
            "extra": "mean: 63.92940717519161 usec\nrounds: 7345"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12299.69440194353,
            "unit": "iter/sec",
            "range": "stddev: 0.000006446044075277268",
            "extra": "mean: 81.30283300713434 usec\nrounds: 6393"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 75036.7334700995,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017907089947310151",
            "extra": "mean: 13.326806135537312 usec\nrounds: 16429"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66124.77037434194,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021765442503573658",
            "extra": "mean: 15.122925861804204 usec\nrounds: 12909"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30562.98999444494,
            "unit": "iter/sec",
            "range": "stddev: 0.00000372998595821547",
            "extra": "mean: 32.71931182720532 usec\nrounds: 8946"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15637.975974097091,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056814826702134106",
            "extra": "mean: 63.946894512206086 usec\nrounds: 4585"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18549.632119311635,
            "unit": "iter/sec",
            "range": "stddev: 0.000005297877540039575",
            "extra": "mean: 53.909424918401534 usec\nrounds: 7236"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22045.874952909886,
            "unit": "iter/sec",
            "range": "stddev: 0.000004607248745388327",
            "extra": "mean: 45.35995972652506 usec\nrounds: 6862"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 61089.91823436874,
            "unit": "iter/sec",
            "range": "stddev: 0.000002238811796512496",
            "extra": "mean: 16.369313119122943 usec\nrounds: 17653"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40543.69949604757,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025183367403757925",
            "extra": "mean: 24.664744767494284 usec\nrounds: 7825"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45154.43143835363,
            "unit": "iter/sec",
            "range": "stddev: 0.000003120585332115828",
            "extra": "mean: 22.14622060661386 usec\nrounds: 12935"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26406.33698909341,
            "unit": "iter/sec",
            "range": "stddev: 0.000004413941877750969",
            "extra": "mean: 37.86969773251888 usec\nrounds: 6586"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23903.47180701766,
            "unit": "iter/sec",
            "range": "stddev: 0.00000473934758339312",
            "extra": "mean: 41.834927079773266 usec\nrounds: 7042"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 116671.264168675,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014090325186292142",
            "extra": "mean: 8.57109080908107 usec\nrounds: 20250"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 93849.00832600679,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013986024440011772",
            "extra": "mean: 10.655413603586123 usec\nrounds: 25400"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 118895.79951008612,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011729055228243358",
            "extra": "mean: 8.410726065349083 usec\nrounds: 17373"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 143101.5942184487,
            "unit": "iter/sec",
            "range": "stddev: 0.000001039768975488046",
            "extra": "mean: 6.9880423447517375 usec\nrounds: 30404"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132091.34441217477,
            "unit": "iter/sec",
            "range": "stddev: 0.000001048568843507412",
            "extra": "mean: 7.570518753141183 usec\nrounds: 28419"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 146080.35478623546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010297595421486677",
            "extra": "mean: 6.845547448617134 usec\nrounds: 27950"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 205992.5019678875,
            "unit": "iter/sec",
            "range": "stddev: 9.348968534339579e-7",
            "extra": "mean: 4.854545628830177 usec\nrounds: 35894"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104680.6227010353,
            "unit": "iter/sec",
            "range": "stddev: 0.00000134354983405084",
            "extra": "mean: 9.552866368171784 usec\nrounds: 17208"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138453.77985429735,
            "unit": "iter/sec",
            "range": "stddev: 0.000001035761713455499",
            "extra": "mean: 7.222626937685313 usec\nrounds: 30657"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87540.15834199241,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014952029741786266",
            "extra": "mean: 11.423328663552425 usec\nrounds: 13027"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50280.48535382698,
            "unit": "iter/sec",
            "range": "stddev: 0.000003739205850356013",
            "extra": "mean: 19.888431723817625 usec\nrounds: 293"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 307697.41404374485,
            "unit": "iter/sec",
            "range": "stddev: 7.573124083918706e-7",
            "extra": "mean: 3.2499460650580305 usec\nrounds: 52225"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 271572.6955756232,
            "unit": "iter/sec",
            "range": "stddev: 7.591009725146227e-7",
            "extra": "mean: 3.6822553087688306 usec\nrounds: 42594"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 319917.7376836748,
            "unit": "iter/sec",
            "range": "stddev: 6.537666743336875e-7",
            "extra": "mean: 3.125803549501123 usec\nrounds: 45889"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 217746.48392696783,
            "unit": "iter/sec",
            "range": "stddev: 8.259340543787325e-7",
            "extra": "mean: 4.592496659259031 usec\nrounds: 43718"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 330696.51196320914,
            "unit": "iter/sec",
            "range": "stddev: 6.258820289408096e-7",
            "extra": "mean: 3.023920615501541 usec\nrounds: 52519"
          }
        ]
      },
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
          "id": "7b7ae561f1aa71620461e1a894df644939b8e368",
          "message": "Merge pull request #65 from amsdal/feature/api-server-template-example\n\nAPI Server example",
          "timestamp": "2024-08-15T20:13:37+03:00",
          "tree_id": "5f8c9c092f24064128db72962572c2c75a55c71f",
          "url": "https://github.com/amsdal/amsdal-glue/commit/7b7ae561f1aa71620461e1a894df644939b8e368"
        },
        "date": 1723742042614,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 76545.55818870083,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024800235892756727",
            "extra": "mean: 13.064115327695312 usec\nrounds: 4305"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59198.68055725598,
            "unit": "iter/sec",
            "range": "stddev: 0.000003111963538281017",
            "extra": "mean: 16.89226838481335 usec\nrounds: 17237"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 80137.62107746175,
            "unit": "iter/sec",
            "range": "stddev: 0.000011599283132805618",
            "extra": "mean: 12.478533634451054 usec\nrounds: 11551"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 43209.24449018072,
            "unit": "iter/sec",
            "range": "stddev: 0.00000719411717362654",
            "extra": "mean: 23.143195670251757 usec\nrounds: 10956"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 150398.92808440363,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014226610137768343",
            "extra": "mean: 6.648983558172713 usec\nrounds: 28679"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68672.47108138712,
            "unit": "iter/sec",
            "range": "stddev: 0.000002256156187656093",
            "extra": "mean: 14.561875876213202 usec\nrounds: 11694"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 85530.5727731414,
            "unit": "iter/sec",
            "range": "stddev: 0.000002533475988235751",
            "extra": "mean: 11.691725748784224 usec\nrounds: 9376"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57664.178960168654,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027686570016347153",
            "extra": "mean: 17.341788577112087 usec\nrounds: 10451"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18704.0325256437,
            "unit": "iter/sec",
            "range": "stddev: 0.000005162695560086639",
            "extra": "mean: 53.46440659943116 usec\nrounds: 6152"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35333.38947982685,
            "unit": "iter/sec",
            "range": "stddev: 0.00000461319685044421",
            "extra": "mean: 28.30184181936288 usec\nrounds: 11390"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21904.572456790316,
            "unit": "iter/sec",
            "range": "stddev: 0.00001543692871634531",
            "extra": "mean: 45.652568748951076 usec\nrounds: 7106"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15721.038083395697,
            "unit": "iter/sec",
            "range": "stddev: 0.000005295212065916495",
            "extra": "mean: 63.60903107640097 usec\nrounds: 7375"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12254.204951570864,
            "unit": "iter/sec",
            "range": "stddev: 0.000006350030423025965",
            "extra": "mean: 81.60464134164903 usec\nrounds: 5725"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 75123.59204317127,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016988093622561612",
            "extra": "mean: 13.311397562370688 usec\nrounds: 16895"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66963.48071524348,
            "unit": "iter/sec",
            "range": "stddev: 0.000001933857835065118",
            "extra": "mean: 14.9335128538556 usec\nrounds: 15480"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30709.767138249183,
            "unit": "iter/sec",
            "range": "stddev: 0.000004442199667072637",
            "extra": "mean: 32.56293007687754 usec\nrounds: 8221"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15561.107268497253,
            "unit": "iter/sec",
            "range": "stddev: 0.00000567304806133642",
            "extra": "mean: 64.26277916767877 usec\nrounds: 5491"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18812.70700400237,
            "unit": "iter/sec",
            "range": "stddev: 0.000004859025670773804",
            "extra": "mean: 53.155561280322495 usec\nrounds: 7332"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22176.569053319698,
            "unit": "iter/sec",
            "range": "stddev: 0.000005068454617173088",
            "extra": "mean: 45.09263798181199 usec\nrounds: 6418"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 61067.73073177633,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024159634979024233",
            "extra": "mean: 16.37526051839444 usec\nrounds: 17652"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40645.075052443215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028114846221693765",
            "extra": "mean: 24.603226804470843 usec\nrounds: 8642"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46237.248629404094,
            "unit": "iter/sec",
            "range": "stddev: 0.000002485447570588068",
            "extra": "mean: 21.62758446150406 usec\nrounds: 12769"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26223.5900086269,
            "unit": "iter/sec",
            "range": "stddev: 0.000004403322321635127",
            "extra": "mean: 38.133604120222486 usec\nrounds: 6703"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24048.473821399075,
            "unit": "iter/sec",
            "range": "stddev: 0.000004412456030867354",
            "extra": "mean: 41.58268035746073 usec\nrounds: 7561"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 118698.40821966602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012706062242238245",
            "extra": "mean: 8.424712807853133 usec\nrounds: 18711"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96439.25285664045,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015136452937906342",
            "extra": "mean: 10.369221767888714 usec\nrounds: 24113"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119750.66848643331,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012539441303358921",
            "extra": "mean: 8.3506840724926 usec\nrounds: 13275"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 146239.6078057858,
            "unit": "iter/sec",
            "range": "stddev: 0.000001180977379434574",
            "extra": "mean: 6.838092737010446 usec\nrounds: 30990"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132541.33150298998,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011426183994933035",
            "extra": "mean: 7.544816312468092 usec\nrounds: 30865"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148094.27629442266,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011214420080202997",
            "extra": "mean: 6.752455429215401 usec\nrounds: 32285"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 205760.5013983649,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010375131647539465",
            "extra": "mean: 4.860019261247516 usec\nrounds: 35905"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102802.95349009748,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013500695876455919",
            "extra": "mean: 9.727346988103072 usec\nrounds: 17421"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138953.79310472077,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010538226198144192",
            "extra": "mean: 7.196636937045415 usec\nrounds: 21064"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88433.20116561072,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014416742558782165",
            "extra": "mean: 11.30797016074629 usec\nrounds: 13198"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49839.526678342365,
            "unit": "iter/sec",
            "range": "stddev: 0.000004755704793359565",
            "extra": "mean: 20.064396005481072 usec\nrounds: 292"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 320022.13840059325,
            "unit": "iter/sec",
            "range": "stddev: 6.610606975278348e-7",
            "extra": "mean: 3.1247838196376048 usec\nrounds: 52008"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 278015.02431275876,
            "unit": "iter/sec",
            "range": "stddev: 8.137093637740982e-7",
            "extra": "mean: 3.596927908741469 usec\nrounds: 44049"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324513.8668370371,
            "unit": "iter/sec",
            "range": "stddev: 6.221411909981604e-7",
            "extra": "mean: 3.0815324156923483 usec\nrounds: 47457"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 219220.14094244727,
            "unit": "iter/sec",
            "range": "stddev: 8.071059088418069e-7",
            "extra": "mean: 4.561624655932203 usec\nrounds: 42227"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 335670.77194131055,
            "unit": "iter/sec",
            "range": "stddev: 5.794831398450202e-7",
            "extra": "mean: 2.979109543010323 usec\nrounds: 53328"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "02c47fcf0e99dcf5ff2b652e9a92903be8e2b085",
          "message": "Merge pull request #66 from amsdal/feature/cqrs\n\nPipelines, Process Parallel Executor, CQRS, Lakehouse",
          "timestamp": "2024-09-16T18:43:25+03:00",
          "tree_id": "51520fea954fa17d52ca84efc2b3ecbef9a92b52",
          "url": "https://github.com/amsdal/amsdal-glue/commit/02c47fcf0e99dcf5ff2b652e9a92903be8e2b085"
        },
        "date": 1726501455204,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 64977.344199459185,
            "unit": "iter/sec",
            "range": "stddev: 0.000005091762488772498",
            "extra": "mean: 15.389979573962382 usec\nrounds: 3545"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 57792.22782986684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034978184863219514",
            "extra": "mean: 17.303364787110752 usec\nrounds: 14821"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 85329.33958949665,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015441730037737066",
            "extra": "mean: 11.719298482922888 usec\nrounds: 11840"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 51037.563915368584,
            "unit": "iter/sec",
            "range": "stddev: 0.000003271024737092009",
            "extra": "mean: 19.593411661618845 usec\nrounds: 9871"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 151738.60058670005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011218881119073506",
            "extra": "mean: 6.590280891832942 usec\nrounds: 24571"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68706.8417464717,
            "unit": "iter/sec",
            "range": "stddev: 0.000002628415981253782",
            "extra": "mean: 14.554591283499843 usec\nrounds: 10963"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 91471.22748979261,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014274313220015247",
            "extra": "mean: 10.932399481701404 usec\nrounds: 10743"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 59165.09319595359,
            "unit": "iter/sec",
            "range": "stddev: 0.000002090077705643526",
            "extra": "mean: 16.901857936537347 usec\nrounds: 9764"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18438.7044626656,
            "unit": "iter/sec",
            "range": "stddev: 0.000005778071781156676",
            "extra": "mean: 54.23374521918198 usec\nrounds: 6109"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36121.17084172816,
            "unit": "iter/sec",
            "range": "stddev: 0.000003445084201621927",
            "extra": "mean: 27.684595396469614 usec\nrounds: 8985"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22166.970406571756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046800003363216985",
            "extra": "mean: 45.11216380311194 usec\nrounds: 7327"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15375.28643823218,
            "unit": "iter/sec",
            "range": "stddev: 0.000006974993350237988",
            "extra": "mean: 65.0394387133758 usec\nrounds: 6933"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12131.771087872155,
            "unit": "iter/sec",
            "range": "stddev: 0.000006696895028349262",
            "extra": "mean: 82.4281955830568 usec\nrounds: 6050"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74202.59800923825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020280169792122882",
            "extra": "mean: 13.476617083885658 usec\nrounds: 11621"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66237.85836819049,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020262200382828567",
            "extra": "mean: 15.097106468047155 usec\nrounds: 17767"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30697.491284039614,
            "unit": "iter/sec",
            "range": "stddev: 0.00000359274013377181",
            "extra": "mean: 32.575951915651316 usec\nrounds: 8085"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15488.651248028664,
            "unit": "iter/sec",
            "range": "stddev: 0.00000588907932079094",
            "extra": "mean: 64.56340090472862 usec\nrounds: 5614"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18619.37349462863,
            "unit": "iter/sec",
            "range": "stddev: 0.000005419578450524476",
            "extra": "mean: 53.70749989458468 usec\nrounds: 7477"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21731.04832112316,
            "unit": "iter/sec",
            "range": "stddev: 0.000004902381024399846",
            "extra": "mean: 46.01710811291019 usec\nrounds: 6641"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 60741.02198771753,
            "unit": "iter/sec",
            "range": "stddev: 0.000001983375064536224",
            "extra": "mean: 16.46333840418771 usec\nrounds: 17261"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40370.53913551427,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025821252755648563",
            "extra": "mean: 24.77053865055501 usec\nrounds: 8699"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45301.43586994481,
            "unit": "iter/sec",
            "range": "stddev: 0.000002427979234440009",
            "extra": "mean: 22.074355498816512 usec\nrounds: 12905"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25766.818416637092,
            "unit": "iter/sec",
            "range": "stddev: 0.000004311567600144219",
            "extra": "mean: 38.80960325914048 usec\nrounds: 6629"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23593.472221706506,
            "unit": "iter/sec",
            "range": "stddev: 0.000004540792255501843",
            "extra": "mean: 42.384604970521394 usec\nrounds: 8464"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115856.44585148308,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012675640964132245",
            "extra": "mean: 8.631371285823015 usec\nrounds: 22226"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 94414.04224831794,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013750061389990883",
            "extra": "mean: 10.591644803957282 usec\nrounds: 23720"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 117882.15748931537,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012172552750363318",
            "extra": "mean: 8.483047997239431 usec\nrounds: 16649"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 146303.61890017294,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010555071912450073",
            "extra": "mean: 6.835100919016419 usec\nrounds: 32854"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132392.0138946398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011452890820548556",
            "extra": "mean: 7.553325692256785 usec\nrounds: 30116"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148289.7541610105,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010120921759639617",
            "extra": "mean: 6.743554237160694 usec\nrounds: 34560"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 207406.51818683598,
            "unit": "iter/sec",
            "range": "stddev: 8.334829955372933e-7",
            "extra": "mean: 4.82144924249285 usec\nrounds: 34414"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 100647.21355353085,
            "unit": "iter/sec",
            "range": "stddev: 0.000025845482836625632",
            "extra": "mean: 9.935694836381474 usec\nrounds: 15178"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137529.10939121837,
            "unit": "iter/sec",
            "range": "stddev: 0.000001150330794902656",
            "extra": "mean: 7.27118792833434 usec\nrounds: 27934"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86863.65840993878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016255800421678832",
            "extra": "mean: 11.51229430472136 usec\nrounds: 12959"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50274.33332005444,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025894639597855783",
            "extra": "mean: 19.890865456809543 usec\nrounds: 9046"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 307424.8216419355,
            "unit": "iter/sec",
            "range": "stddev: 6.665298610487388e-7",
            "extra": "mean: 3.2528277796798144 usec\nrounds: 46843"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 274451.6362950096,
            "unit": "iter/sec",
            "range": "stddev: 6.731730943098254e-7",
            "extra": "mean: 3.6436292146026577 usec\nrounds: 40676"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 323871.66497117036,
            "unit": "iter/sec",
            "range": "stddev: 6.361460436625485e-7",
            "extra": "mean: 3.0876427553148735 usec\nrounds: 45251"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 215650.76174089243,
            "unit": "iter/sec",
            "range": "stddev: 8.186182645510157e-7",
            "extra": "mean: 4.637127139859189 usec\nrounds: 40858"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331155.295650952,
            "unit": "iter/sec",
            "range": "stddev: 6.590182915841425e-7",
            "extra": "mean: 3.019731265460514 usec\nrounds: 56996"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "161331703+OlehKyrtsun@users.noreply.github.com",
            "name": "OlehKyrtsun",
            "username": "OlehKyrtsun"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "e940cb8bd56965cb6188e11cad9ba3ec203fb249",
          "message": "Merge pull request #67 from amsdal/release/16-09-24\n\nRelease/16 09 24",
          "timestamp": "2024-09-16T19:06:18+03:00",
          "tree_id": "4f1510e22447096b99bcab388962b7e54806ffa3",
          "url": "https://github.com/amsdal/amsdal-glue/commit/e940cb8bd56965cb6188e11cad9ba3ec203fb249"
        },
        "date": 1726502839458,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 76378.69304938249,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023439584044031765",
            "extra": "mean: 13.092656604551378 usec\nrounds: 4384"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 53197.37760574689,
            "unit": "iter/sec",
            "range": "stddev: 0.000005542503438311116",
            "extra": "mean: 18.797919089379516 usec\nrounds: 14375"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 85576.62288567731,
            "unit": "iter/sec",
            "range": "stddev: 0.000001930304207201272",
            "extra": "mean: 11.685434249209743 usec\nrounds: 13980"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 46021.95227776095,
            "unit": "iter/sec",
            "range": "stddev: 0.000006145421278948399",
            "extra": "mean: 21.72876096095617 usec\nrounds: 9921"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 133806.32940209794,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025330209641595666",
            "extra": "mean: 7.473488021593701 usec\nrounds: 17365"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 60066.14329223116,
            "unit": "iter/sec",
            "range": "stddev: 0.000005000885707827089",
            "extra": "mean: 16.648313761961443 usec\nrounds: 11015"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 89942.56356879987,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019003698800262587",
            "extra": "mean: 11.11820655673294 usec\nrounds: 10703"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57435.95478746198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029987165439961266",
            "extra": "mean: 17.410696900581435 usec\nrounds: 11247"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18263.137262198583,
            "unit": "iter/sec",
            "range": "stddev: 0.000008436647884608003",
            "extra": "mean: 54.75510508645306 usec\nrounds: 6335"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36062.09424860535,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035433805633525742",
            "extra": "mean: 27.729948047558935 usec\nrounds: 10028"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22294.019880515716,
            "unit": "iter/sec",
            "range": "stddev: 0.000004875896814054097",
            "extra": "mean: 44.85507796976395 usec\nrounds: 7790"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15724.04030774204,
            "unit": "iter/sec",
            "range": "stddev: 0.000006047705175618149",
            "extra": "mean: 63.59688606926493 usec\nrounds: 6944"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12301.994845408462,
            "unit": "iter/sec",
            "range": "stddev: 0.000007203423912920564",
            "extra": "mean: 81.28762957279527 usec\nrounds: 6330"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74717.96701208023,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019189736146225484",
            "extra": "mean: 13.383661788312873 usec\nrounds: 15700"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 67236.20737634518,
            "unit": "iter/sec",
            "range": "stddev: 0.00000194579148094443",
            "extra": "mean: 14.872938837888954 usec\nrounds: 11663"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30749.38799390552,
            "unit": "iter/sec",
            "range": "stddev: 0.000004086998613896776",
            "extra": "mean: 32.52097245636884 usec\nrounds: 8337"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15519.2648575475,
            "unit": "iter/sec",
            "range": "stddev: 0.000006314463322133809",
            "extra": "mean: 64.43604186017025 usec\nrounds: 5580"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18546.289416076652,
            "unit": "iter/sec",
            "range": "stddev: 0.000005424247236234873",
            "extra": "mean: 53.919141320697854 usec\nrounds: 7004"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22113.177468358186,
            "unit": "iter/sec",
            "range": "stddev: 0.000004934809902921633",
            "extra": "mean: 45.22190451512014 usec\nrounds: 6909"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct",
            "value": 61311.87847225639,
            "unit": "iter/sec",
            "range": "stddev: 0.00000207539545937233",
            "extra": "mean: 16.310053205309963 usec\nrounds: 16973"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40587.02410262891,
            "unit": "iter/sec",
            "range": "stddev: 0.000002758957158419109",
            "extra": "mean: 24.638416393165123 usec\nrounds: 8254"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45697.59739201213,
            "unit": "iter/sec",
            "range": "stddev: 0.00000241659826236141",
            "extra": "mean: 21.88298853923551 usec\nrounds: 12548"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26576.662862950507,
            "unit": "iter/sec",
            "range": "stddev: 0.000004490945033987016",
            "extra": "mean: 37.62699648021126 usec\nrounds: 6798"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23984.354309138762,
            "unit": "iter/sec",
            "range": "stddev: 0.000004865836694241048",
            "extra": "mean: 41.693847043402364 usec\nrounds: 8172"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115492.61794810215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012866599056433607",
            "extra": "mean: 8.658562060212027 usec\nrounds: 21297"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95760.01377416277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013838167490468196",
            "extra": "mean: 10.44277209857516 usec\nrounds: 23933"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 121359.17042141625,
            "unit": "iter/sec",
            "range": "stddev: 0.00000114890330344455",
            "extra": "mean: 8.240003590396414 usec\nrounds: 17240"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 146781.02734308763,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011937771754599423",
            "extra": "mean: 6.812869606523388 usec\nrounds: 32041"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 134445.54566458243,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011705567393924542",
            "extra": "mean: 7.43795560542274 usec\nrounds: 31832"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 149274.84665050104,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010147923732599379",
            "extra": "mean: 6.6990522679370885 usec\nrounds: 32100"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 207775.32547612189,
            "unit": "iter/sec",
            "range": "stddev: 8.59076460618238e-7",
            "extra": "mean: 4.812891028847998 usec\nrounds: 34824"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102424.62095883615,
            "unit": "iter/sec",
            "range": "stddev: 0.000025524482407555276",
            "extra": "mean: 9.763277526815491 usec\nrounds: 15548"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138965.7133160722,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011631511693812728",
            "extra": "mean: 7.196019623383923 usec\nrounds: 29862"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86011.72590187585,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018529750696586608",
            "extra": "mean: 11.626321754557315 usec\nrounds: 12958"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50346.77840732596,
            "unit": "iter/sec",
            "range": "stddev: 0.000003032593896538034",
            "extra": "mean: 19.86224405282881 usec\nrounds: 8999"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 310514.0209890648,
            "unit": "iter/sec",
            "range": "stddev: 6.178676186128101e-7",
            "extra": "mean: 3.2204664923495234 usec\nrounds: 44662"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 278873.3292423541,
            "unit": "iter/sec",
            "range": "stddev: 6.50745121949355e-7",
            "extra": "mean: 3.5858574311025375 usec\nrounds: 40030"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 330108.03225897386,
            "unit": "iter/sec",
            "range": "stddev: 6.630783412834639e-7",
            "extra": "mean: 3.0293113231958184 usec\nrounds: 43820"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220328.9057050387,
            "unit": "iter/sec",
            "range": "stddev: 9.802082422263814e-7",
            "extra": "mean: 4.538669117427251 usec\nrounds: 40636"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 334187.2737339723,
            "unit": "iter/sec",
            "range": "stddev: 6.073433682753341e-7",
            "extra": "mean: 2.992334174867604 usec\nrounds: 55801"
          }
        ]
      },
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
          "id": "90ae41194201036d7b3ce1ca8f3d8bc22f407df4",
          "message": "Merge pull request #69 from amsdal/feature/fixes-and-improvements\n\nFixes and improvements",
          "timestamp": "2024-10-14T15:23:21+03:00",
          "tree_id": "9d1dd2d96526056e9dc1a386df40e8f1ff21ac85",
          "url": "https://github.com/amsdal/amsdal-glue/commit/90ae41194201036d7b3ce1ca8f3d8bc22f407df4"
        },
        "date": 1728908627983,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 77646.27128007349,
            "unit": "iter/sec",
            "range": "stddev: 0.00000199566520752211",
            "extra": "mean: 12.87891850457257 usec\nrounds: 5609"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59503.88219703532,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036333827411858333",
            "extra": "mean: 16.805626172233573 usec\nrounds: 14569"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 87773.96649532433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014428737337729964",
            "extra": "mean: 11.392899739278269 usec\nrounds: 14053"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 51868.64370426936,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023254236471196554",
            "extra": "mean: 19.279470766606703 usec\nrounds: 9879"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 158881.15655809766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010959081226486455",
            "extra": "mean: 6.2940125919484515 usec\nrounds: 26079"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68835.29560627398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018601582486174082",
            "extra": "mean: 14.527430894171319 usec\nrounds: 10250"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 91013.72321361271,
            "unit": "iter/sec",
            "range": "stddev: 0.000001647075076702806",
            "extra": "mean: 10.987354046081176 usec\nrounds: 8054"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 55400.17836128674,
            "unit": "iter/sec",
            "range": "stddev: 0.000003850912659528028",
            "extra": "mean: 18.050483402392675 usec\nrounds: 11446"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16655.02444477424,
            "unit": "iter/sec",
            "range": "stddev: 0.000017649193645027297",
            "extra": "mean: 60.041941296205344 usec\nrounds: 6347"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 34935.92829423193,
            "unit": "iter/sec",
            "range": "stddev: 0.000004578563586998365",
            "extra": "mean: 28.623827928027442 usec\nrounds: 10750"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21925.4138923807,
            "unit": "iter/sec",
            "range": "stddev: 0.000004495962218560761",
            "extra": "mean: 45.6091732137157 usec\nrounds: 8462"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15154.324424359898,
            "unit": "iter/sec",
            "range": "stddev: 0.000007693437176410427",
            "extra": "mean: 65.98776507599011 usec\nrounds: 7377"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12147.596124875465,
            "unit": "iter/sec",
            "range": "stddev: 0.000006358199231225062",
            "extra": "mean: 82.32081390590781 usec\nrounds: 6275"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74756.2100104375,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018162759310908093",
            "extra": "mean: 13.376815114896536 usec\nrounds: 16851"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66244.2718419994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022205850462109766",
            "extra": "mean: 15.095644833792134 usec\nrounds: 13514"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30636.768589983007,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036606778045988945",
            "extra": "mean: 32.640518110221315 usec\nrounds: 8485"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15617.942068292296,
            "unit": "iter/sec",
            "range": "stddev: 0.000005787856242924793",
            "extra": "mean: 64.02892235272215 usec\nrounds: 4894"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18206.86325055897,
            "unit": "iter/sec",
            "range": "stddev: 0.00006668778745495627",
            "extra": "mean: 54.92434288313221 usec\nrounds: 7573"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21674.860882275978,
            "unit": "iter/sec",
            "range": "stddev: 0.000004941658027291241",
            "extra": "mean: 46.13639761894493 usec\nrounds: 7243"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 71919.04252766374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018754244208151885",
            "extra": "mean: 13.904523264688192 usec\nrounds: 19131"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51777.657261575005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022712434823450083",
            "extra": "mean: 19.31334967412895 usec\nrounds: 15115"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 60253.472840496135,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019718010534280225",
            "extra": "mean: 16.59655373968592 usec\nrounds: 17343"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 47644.70322132014,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023133664561315747",
            "extra": "mean: 20.98869197179757 usec\nrounds: 15016"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41092.95896544263,
            "unit": "iter/sec",
            "range": "stddev: 0.000004974384279631097",
            "extra": "mean: 24.3350691986176 usec\nrounds: 8549"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46173.76040225112,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023721813513909905",
            "extra": "mean: 21.65732206535309 usec\nrounds: 12537"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25909.247644415904,
            "unit": "iter/sec",
            "range": "stddev: 0.000004224229292080584",
            "extra": "mean: 38.5962577425719 usec\nrounds: 5572"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23755.111889752705,
            "unit": "iter/sec",
            "range": "stddev: 0.00000457816869906466",
            "extra": "mean: 42.096202478059986 usec\nrounds: 6992"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117883.75435715483,
            "unit": "iter/sec",
            "range": "stddev: 0.000001233191779977463",
            "extra": "mean: 8.482933084827613 usec\nrounds: 19367"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96498.80098373053,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013437879168448946",
            "extra": "mean: 10.362823058999433 usec\nrounds: 24518"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 121489.46147301004,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011441997303295132",
            "extra": "mean: 8.231166620342282 usec\nrounds: 17902"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 148910.87548193726,
            "unit": "iter/sec",
            "range": "stddev: 9.780175082266302e-7",
            "extra": "mean: 6.715426235750652 usec\nrounds: 31086"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 135408.6315875277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010446960739949223",
            "extra": "mean: 7.385053583926097 usec\nrounds: 28182"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 151741.21865279056,
            "unit": "iter/sec",
            "range": "stddev: 0.000001034344054259564",
            "extra": "mean: 6.590167186466113 usec\nrounds: 22963"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 210430.50230314292,
            "unit": "iter/sec",
            "range": "stddev: 7.875147848280714e-7",
            "extra": "mean: 4.7521627760951475 usec\nrounds: 32999"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 106106.69214652899,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012827925687051606",
            "extra": "mean: 9.4244762490479 usec\nrounds: 12784"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 142032.42246806627,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010602160407057214",
            "extra": "mean: 7.040645949869891 usec\nrounds: 30224"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86759.32699521293,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015781749302962427",
            "extra": "mean: 11.526138279693852 usec\nrounds: 13252"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48019.108227577715,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026914183555304967",
            "extra": "mean: 20.825043132010787 usec\nrounds: 8294"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 318513.41052431177,
            "unit": "iter/sec",
            "range": "stddev: 6.891774566614563e-7",
            "extra": "mean: 3.139585232389049 usec\nrounds: 44665"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 282573.9721312753,
            "unit": "iter/sec",
            "range": "stddev: 6.490642401638575e-7",
            "extra": "mean: 3.5388963550239168 usec\nrounds: 40382"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 332322.2170565573,
            "unit": "iter/sec",
            "range": "stddev: 5.908627210681003e-7",
            "extra": "mean: 3.0091277340925173 usec\nrounds: 50985"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220327.72248251876,
            "unit": "iter/sec",
            "range": "stddev: 8.450121047690867e-7",
            "extra": "mean: 4.538693491370982 usec\nrounds: 42319"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 338545.7094465096,
            "unit": "iter/sec",
            "range": "stddev: 6.600926710247691e-7",
            "extra": "mean: 2.9538108801759915 usec\nrounds: 58569"
          }
        ]
      },
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
          "id": "651f8fdfc34e55ba0cbb605e60841afbddbbbf8d",
          "message": "Merge pull request #70 from amsdal/feature/postgres-update-fix\n\nFixed postgres field update to DOUBLE PRECISION and BIGINT",
          "timestamp": "2024-10-15T15:35:31+03:00",
          "tree_id": "66cb30c05196b9131a8b9f49e5e581675e71bf17",
          "url": "https://github.com/amsdal/amsdal-glue/commit/651f8fdfc34e55ba0cbb605e60841afbddbbbf8d"
        },
        "date": 1728995780745,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 67883.03598101465,
            "unit": "iter/sec",
            "range": "stddev: 0.000004064484805641201",
            "extra": "mean: 14.73122092358505 usec\nrounds: 4621"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 38149.717977337794,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051260118071614875",
            "extra": "mean: 26.212513565474676 usec\nrounds: 9669"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 84693.647718829,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015355151958473943",
            "extra": "mean: 11.807260956805868 usec\nrounds: 15514"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 50283.608516220884,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025909628529701612",
            "extra": "mean: 19.887196434548088 usec\nrounds: 9915"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 154787.04049758092,
            "unit": "iter/sec",
            "range": "stddev: 0.000002464755324548542",
            "extra": "mean: 6.4604891778109055 usec\nrounds: 23497"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 67802.2224795597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019505069338924147",
            "extra": "mean: 14.748779072861062 usec\nrounds: 10684"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 89171.49925368786,
            "unit": "iter/sec",
            "range": "stddev: 0.000004242668372008479",
            "extra": "mean: 11.214345484481054 usec\nrounds: 9834"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58613.934207249156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019968834432782356",
            "extra": "mean: 17.060789614704344 usec\nrounds: 11977"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17112.09304099041,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051375163748048726",
            "extra": "mean: 58.43820493522294 usec\nrounds: 5485"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35198.023350682786,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032572429865771316",
            "extra": "mean: 28.410686305786587 usec\nrounds: 9536"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21295.00855221101,
            "unit": "iter/sec",
            "range": "stddev: 0.000004735483860661805",
            "extra": "mean: 46.95936127699617 usec\nrounds: 8296"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15043.023467607447,
            "unit": "iter/sec",
            "range": "stddev: 0.000005712502077145707",
            "extra": "mean: 66.47599813650011 usec\nrounds: 6959"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11774.748084675843,
            "unit": "iter/sec",
            "range": "stddev: 0.0000072034071361915234",
            "extra": "mean: 84.92750696734161 usec\nrounds: 5961"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73949.0080068207,
            "unit": "iter/sec",
            "range": "stddev: 0.000001871202103973323",
            "extra": "mean: 13.522831839850573 usec\nrounds: 16033"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 64775.36565251444,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019280898927575003",
            "extra": "mean: 15.437967658329724 usec\nrounds: 16833"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 29884.438505704464,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038426090956683885",
            "extra": "mean: 33.46223151588128 usec\nrounds: 8410"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15322.17590722526,
            "unit": "iter/sec",
            "range": "stddev: 0.000005885104157211956",
            "extra": "mean: 65.26488183238024 usec\nrounds: 5129"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17940.635983677465,
            "unit": "iter/sec",
            "range": "stddev: 0.000005431254814939297",
            "extra": "mean: 55.739384094845256 usec\nrounds: 6896"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21298.701395786175,
            "unit": "iter/sec",
            "range": "stddev: 0.000005120188814880882",
            "extra": "mean: 46.951219298179566 usec\nrounds: 5061"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 71128.33961712202,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018333124528382136",
            "extra": "mean: 14.059093820872487 usec\nrounds: 18600"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 50879.394882054745,
            "unit": "iter/sec",
            "range": "stddev: 0.00000231406329111839",
            "extra": "mean: 19.654321799976866 usec\nrounds: 14378"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 59275.56171836269,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020835399477777285",
            "extra": "mean: 16.87035889683041 usec\nrounds: 16671"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 46305.847644257956,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023999015982525757",
            "extra": "mean: 21.595544642275918 usec\nrounds: 15192"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40678.60526861174,
            "unit": "iter/sec",
            "range": "stddev: 0.000002650780978934562",
            "extra": "mean: 24.58294706509065 usec\nrounds: 6067"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45617.976791089946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023288378535154742",
            "extra": "mean: 21.92118262016651 usec\nrounds: 12557"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25637.565441033403,
            "unit": "iter/sec",
            "range": "stddev: 0.00000438039449336243",
            "extra": "mean: 39.00526367450949 usec\nrounds: 5858"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23454.890878855702,
            "unit": "iter/sec",
            "range": "stddev: 0.000004585811029",
            "extra": "mean: 42.63503101186831 usec\nrounds: 7767"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117070.39540191555,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013196209667243134",
            "extra": "mean: 8.541869159721296 usec\nrounds: 21032"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95057.27784491122,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013999636304912958",
            "extra": "mean: 10.519973038061638 usec\nrounds: 23226"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119148.34177348226,
            "unit": "iter/sec",
            "range": "stddev: 0.000001175303287861018",
            "extra": "mean: 8.39289901240204 usec\nrounds: 17418"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 145793.94918025742,
            "unit": "iter/sec",
            "range": "stddev: 0.000001017123370709584",
            "extra": "mean: 6.858995216348898 usec\nrounds: 30224"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132815.2126142161,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011112471750286682",
            "extra": "mean: 7.529257984208981 usec\nrounds: 18631"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 150402.37511954166,
            "unit": "iter/sec",
            "range": "stddev: 0.00000101610530331244",
            "extra": "mean: 6.648831171749699 usec\nrounds: 20178"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 208447.5129261365,
            "unit": "iter/sec",
            "range": "stddev: 8.143442052071467e-7",
            "extra": "mean: 4.797370743177687 usec\nrounds: 36770"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103477.09329142176,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013665766468877021",
            "extra": "mean: 9.663974587918773 usec\nrounds: 16495"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138915.46476759695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010598957960237826",
            "extra": "mean: 7.198622570013942 usec\nrounds: 27633"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86284.38851609119,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015400760699044425",
            "extra": "mean: 11.589582046044283 usec\nrounds: 10440"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 47730.13100001057,
            "unit": "iter/sec",
            "range": "stddev: 0.000002914327341879393",
            "extra": "mean: 20.95112623930947 usec\nrounds: 9343"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 316773.7197922709,
            "unit": "iter/sec",
            "range": "stddev: 7.175125212453041e-7",
            "extra": "mean: 3.1568275318286028 usec\nrounds: 43409"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 271321.41599305585,
            "unit": "iter/sec",
            "range": "stddev: 7.827159680175738e-7",
            "extra": "mean: 3.685665565100817 usec\nrounds: 36323"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 323505.3147882185,
            "unit": "iter/sec",
            "range": "stddev: 6.315100880715035e-7",
            "extra": "mean: 3.0911393237995064 usec\nrounds: 42699"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220216.6708483749,
            "unit": "iter/sec",
            "range": "stddev: 8.162785001503322e-7",
            "extra": "mean: 4.5409822796228125 usec\nrounds: 42070"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 333644.9553866426,
            "unit": "iter/sec",
            "range": "stddev: 7.299698182160452e-7",
            "extra": "mean: 2.997198020995569 usec\nrounds: 53373"
          }
        ]
      },
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
          "id": "7b8ce81673149c84d9808fb8ba1028c9013cdc7d",
          "message": "Merge pull request #71 from amsdal/feature/exception-fixes\n\nException fixes",
          "timestamp": "2024-10-18T12:39:29+03:00",
          "tree_id": "48edb0603527f3888c21d05d6878189d10b4a33b",
          "url": "https://github.com/amsdal/amsdal-glue/commit/7b8ce81673149c84d9808fb8ba1028c9013cdc7d"
        },
        "date": 1729244418179,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 68760.67952527915,
            "unit": "iter/sec",
            "range": "stddev: 0.000003838203668650272",
            "extra": "mean: 14.54319542657167 usec\nrounds: 4432"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 49491.89336558886,
            "unit": "iter/sec",
            "range": "stddev: 0.0000060176261737698375",
            "extra": "mean: 20.205329236712704 usec\nrounds: 10369"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 82596.22805728868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026599740682957546",
            "extra": "mean: 12.107090402559312 usec\nrounds: 17295"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 49966.84045027417,
            "unit": "iter/sec",
            "range": "stddev: 0.000002842741157995398",
            "extra": "mean: 20.013272622173833 usec\nrounds: 8082"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 154965.56845426903,
            "unit": "iter/sec",
            "range": "stddev: 9.608209629415442e-7",
            "extra": "mean: 6.453046376525274 usec\nrounds: 26440"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 66669.74273934095,
            "unit": "iter/sec",
            "range": "stddev: 0.000002237188927175566",
            "extra": "mean: 14.999307915581817 usec\nrounds: 11066"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 90291.16999624457,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014950603632088982",
            "extra": "mean: 11.075280119214232 usec\nrounds: 11263"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57097.884345416096,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029375959663363776",
            "extra": "mean: 17.513783767371436 usec\nrounds: 12108"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17094.195318413094,
            "unit": "iter/sec",
            "range": "stddev: 0.000005188730986768422",
            "extra": "mean: 58.499390077919905 usec\nrounds: 6559"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35272.15620128286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032641751487251374",
            "extra": "mean: 28.35097447100866 usec\nrounds: 11087"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21618.036243245853,
            "unit": "iter/sec",
            "range": "stddev: 0.000004810794589610971",
            "extra": "mean: 46.25767062040296 usec\nrounds: 7956"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15238.7668400815,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057592719916207055",
            "extra": "mean: 65.62210777907353 usec\nrounds: 7288"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11913.100837086185,
            "unit": "iter/sec",
            "range": "stddev: 0.000007434304255965716",
            "extra": "mean: 83.94120167999763 usec\nrounds: 6324"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74444.23654489705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018614109859711745",
            "extra": "mean: 13.432873334618774 usec\nrounds: 16832"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65846.22630576564,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020673010055424473",
            "extra": "mean: 15.186899175609062 usec\nrounds: 16278"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30426.6796959055,
            "unit": "iter/sec",
            "range": "stddev: 0.000003943281183625271",
            "extra": "mean: 32.86589302527707 usec\nrounds: 8460"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15387.0046470157,
            "unit": "iter/sec",
            "range": "stddev: 0.000006707555270961655",
            "extra": "mean: 64.9899069338326 usec\nrounds: 6036"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18285.196992821588,
            "unit": "iter/sec",
            "range": "stddev: 0.000005134487768788085",
            "extra": "mean: 54.68904712334138 usec\nrounds: 7501"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21816.842806780885,
            "unit": "iter/sec",
            "range": "stddev: 0.000004746840439162754",
            "extra": "mean: 45.83614635978356 usec\nrounds: 7316"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 71858.99716430814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017509909722573783",
            "extra": "mean: 13.916141881488612 usec\nrounds: 19283"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51574.2926661515,
            "unit": "iter/sec",
            "range": "stddev: 0.000002258230531894481",
            "extra": "mean: 19.389504892934877 usec\nrounds: 13718"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 60047.780513032885,
            "unit": "iter/sec",
            "range": "stddev: 0.000002132837845542969",
            "extra": "mean: 16.65340486286513 usec\nrounds: 17605"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 46869.882689876,
            "unit": "iter/sec",
            "range": "stddev: 0.000002412967786610903",
            "extra": "mean: 21.335662532306745 usec\nrounds: 14861"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40470.54022325991,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027565673267767956",
            "extra": "mean: 24.709331639345482 usec\nrounds: 9121"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44978.063321555856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024516584025112156",
            "extra": "mean: 22.233060433278983 usec\nrounds: 14111"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25671.152768800708,
            "unit": "iter/sec",
            "range": "stddev: 0.000004395663013565901",
            "extra": "mean: 38.95423041599224 usec\nrounds: 6686"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23138.404158260324,
            "unit": "iter/sec",
            "range": "stddev: 0.000006377343164175061",
            "extra": "mean: 43.218192281553854 usec\nrounds: 10387"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117281.19869934923,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011990166695979713",
            "extra": "mean: 8.526515853265652 usec\nrounds: 18906"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95322.13328815081,
            "unit": "iter/sec",
            "range": "stddev: 0.000001534228164307679",
            "extra": "mean: 10.490742973377273 usec\nrounds: 25265"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119076.0997443014,
            "unit": "iter/sec",
            "range": "stddev: 0.000001191760727765698",
            "extra": "mean: 8.397990882699002 usec\nrounds: 17548"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 148012.79948832694,
            "unit": "iter/sec",
            "range": "stddev: 9.652507009249549e-7",
            "extra": "mean: 6.756172462496158 usec\nrounds: 33327"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 134784.95308730577,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010536747466760795",
            "extra": "mean: 7.419225789634388 usec\nrounds: 25445"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148708.70305353816,
            "unit": "iter/sec",
            "range": "stddev: 0.000001012508782387162",
            "extra": "mean: 6.7245559907813846 usec\nrounds: 26038"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 206248.75457164057,
            "unit": "iter/sec",
            "range": "stddev: 8.753576106570411e-7",
            "extra": "mean: 4.84851412594906 usec\nrounds: 37938"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103742.80850487224,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013275488144017348",
            "extra": "mean: 9.6392223655005 usec\nrounds: 17843"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 140280.2210750649,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010225352044546798",
            "extra": "mean: 7.128588708631226 usec\nrounds: 32671"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86785.27979210662,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015735264845172578",
            "extra": "mean: 11.522691433333986 usec\nrounds: 13075"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49181.347752553425,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028130504546247675",
            "extra": "mean: 20.332911676827347 usec\nrounds: 9833"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 312306.438412592,
            "unit": "iter/sec",
            "range": "stddev: 6.558220719790766e-7",
            "extra": "mean: 3.2019832991047315 usec\nrounds: 43477"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 275200.9693721693,
            "unit": "iter/sec",
            "range": "stddev: 6.617098361010263e-7",
            "extra": "mean: 3.6337081307575096 usec\nrounds: 45512"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 322329.7438697876,
            "unit": "iter/sec",
            "range": "stddev: 6.037628802553054e-7",
            "extra": "mean: 3.102413038258029 usec\nrounds: 45721"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 217327.9684212517,
            "unit": "iter/sec",
            "range": "stddev: 7.679835204469157e-7",
            "extra": "mean: 4.60134057877759 usec\nrounds: 45101"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 325523.78547451796,
            "unit": "iter/sec",
            "range": "stddev: 6.218370638811844e-7",
            "extra": "mean: 3.071972140353105 usec\nrounds: 64899"
          }
        ]
      },
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
          "id": "f43f493c3aba87976914d2f8a51da4bc105d28f7",
          "message": "Merge pull request #72 from amsdal/feature/jsonb-field\n\nJSONB field in postgres connection",
          "timestamp": "2024-10-18T13:30:41+03:00",
          "tree_id": "db89194530f5be0fee7a4abf0b96e73c6d3226b6",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f43f493c3aba87976914d2f8a51da4bc105d28f7"
        },
        "date": 1729247490912,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 74639.14967849314,
            "unit": "iter/sec",
            "range": "stddev: 0.000002794218075379493",
            "extra": "mean: 13.39779464674347 usec\nrounds: 4619"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59875.21820424574,
            "unit": "iter/sec",
            "range": "stddev: 0.000004250135571649524",
            "extra": "mean: 16.701400512459262 usec\nrounds: 15096"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 81926.15202202117,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027008008167729286",
            "extra": "mean: 12.206114596120749 usec\nrounds: 14679"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 42433.651595502604,
            "unit": "iter/sec",
            "range": "stddev: 0.000007328896644850373",
            "extra": "mean: 23.56620187987749 usec\nrounds: 6630"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 145683.57989423108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017459689619448708",
            "extra": "mean: 6.864191563153639 usec\nrounds: 26585"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 65857.16122308392,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029548599344612747",
            "extra": "mean: 15.18437754419158 usec\nrounds: 11043"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 91258.49324751589,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015560943316993732",
            "extra": "mean: 10.957884186053233 usec\nrounds: 10920"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57646.560519703984,
            "unit": "iter/sec",
            "range": "stddev: 0.000002460273463512851",
            "extra": "mean: 17.34708872454226 usec\nrounds: 11032"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17404.771583312126,
            "unit": "iter/sec",
            "range": "stddev: 0.000005608746545293141",
            "extra": "mean: 57.45550840545418 usec\nrounds: 5714"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35437.34446688617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035994374072303553",
            "extra": "mean: 28.218818736105728 usec\nrounds: 9741"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21717.7668953149,
            "unit": "iter/sec",
            "range": "stddev: 0.000005094324154999504",
            "extra": "mean: 46.045249717443404 usec\nrounds: 7055"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15371.659193191404,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061705772050775874",
            "extra": "mean: 65.0547860469696 usec\nrounds: 6946"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12090.137409023535,
            "unit": "iter/sec",
            "range": "stddev: 0.000007222398498603521",
            "extra": "mean: 82.71204587415565 usec\nrounds: 5966"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74570.66942487597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019217836401043226",
            "extra": "mean: 13.410098202315597 usec\nrounds: 16351"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65555.35491795893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021633683171930596",
            "extra": "mean: 15.25428397499301 usec\nrounds: 16761"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30162.89487279869,
            "unit": "iter/sec",
            "range": "stddev: 0.000003925992252544218",
            "extra": "mean: 33.15331649091194 usec\nrounds: 8252"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15649.744573499102,
            "unit": "iter/sec",
            "range": "stddev: 0.000005640660328443145",
            "extra": "mean: 63.89880648233555 usec\nrounds: 5470"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18178.6062422149,
            "unit": "iter/sec",
            "range": "stddev: 0.000005164129854041392",
            "extra": "mean: 55.0097178340202 usec\nrounds: 7335"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21763.74170834748,
            "unit": "iter/sec",
            "range": "stddev: 0.000005025843899726129",
            "extra": "mean: 45.947981436319395 usec\nrounds: 6032"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 73034.49682410934,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017226555325265113",
            "extra": "mean: 13.69215978044352 usec\nrounds: 18271"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51489.384121809315,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021991950540782837",
            "extra": "mean: 19.42147914673601 usec\nrounds: 15381"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 60527.63032546266,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020125678831707475",
            "extra": "mean: 16.521380312146825 usec\nrounds: 16708"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 46787.63812564526,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024924995219592103",
            "extra": "mean: 21.373166931713094 usec\nrounds: 13155"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40577.838408810254,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025444865131053074",
            "extra": "mean: 24.643993845243372 usec\nrounds: 8299"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45545.25829057669,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025407254864632012",
            "extra": "mean: 21.956182433307223 usec\nrounds: 12831"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25874.619653123835,
            "unit": "iter/sec",
            "range": "stddev: 0.000004229544448315187",
            "extra": "mean: 38.647911096125824 usec\nrounds: 6612"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23312.882909249976,
            "unit": "iter/sec",
            "range": "stddev: 0.00000498606533775446",
            "extra": "mean: 42.89473781053585 usec\nrounds: 8390"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 118018.64143531278,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014001661967187635",
            "extra": "mean: 8.47323768379515 usec\nrounds: 22214"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95622.17871585565,
            "unit": "iter/sec",
            "range": "stddev: 0.000001360505403046563",
            "extra": "mean: 10.457824883613368 usec\nrounds: 23956"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119254.89132836988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012438660154324",
            "extra": "mean: 8.385400287242618 usec\nrounds: 16502"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 146762.28338658414,
            "unit": "iter/sec",
            "range": "stddev: 9.93987635004966e-7",
            "extra": "mean: 6.813739721982359 usec\nrounds: 31685"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 136226.59188374848,
            "unit": "iter/sec",
            "range": "stddev: 0.000001060425270518602",
            "extra": "mean: 7.340710695114275 usec\nrounds: 29333"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 151903.85320653184,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011529233646457496",
            "extra": "mean: 6.583111480657293 usec\nrounds: 22059"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 210328.29100172833,
            "unit": "iter/sec",
            "range": "stddev: 7.778591763687191e-7",
            "extra": "mean: 4.754472140848531 usec\nrounds: 34357"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 105384.93672284596,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013236824123518125",
            "extra": "mean: 9.489022161012638 usec\nrounds: 17364"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 140415.75444393893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010346746870880103",
            "extra": "mean: 7.121707987541031 usec\nrounds: 28984"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88780.75442674947,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014184698141045849",
            "extra": "mean: 11.263702437053203 usec\nrounds: 11417"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49445.89418894519,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025371345859866314",
            "extra": "mean: 20.2241261160886 usec\nrounds: 8656"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 319900.56120831385,
            "unit": "iter/sec",
            "range": "stddev: 6.296689450622202e-7",
            "extra": "mean: 3.1259713838039094 usec\nrounds: 41278"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 279000.881737915,
            "unit": "iter/sec",
            "range": "stddev: 6.563082077113427e-7",
            "extra": "mean: 3.5842180632940432 usec\nrounds: 38968"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 330962.0697915493,
            "unit": "iter/sec",
            "range": "stddev: 6.686538497298387e-7",
            "extra": "mean: 3.021494277667023 usec\nrounds: 43166"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 216050.11744030644,
            "unit": "iter/sec",
            "range": "stddev: 8.427738381996433e-7",
            "extra": "mean: 4.628555688132384 usec\nrounds: 39644"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 341456.58808532514,
            "unit": "iter/sec",
            "range": "stddev: 7.07624249629659e-7",
            "extra": "mean: 2.928629977846889 usec\nrounds: 57236"
          }
        ]
      },
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
          "id": "ca495709a6bde276b14862092128bc83e5eaa086",
          "message": "Merge pull request #73 from amsdal/bugfix/thread-safe-container-switch\n\nBugfix/thread safe container switch",
          "timestamp": "2024-10-25T13:42:22+03:00",
          "tree_id": "d98706e6776e225f79ba5afddd92c2a2c14c3b30",
          "url": "https://github.com/amsdal/amsdal-glue/commit/ca495709a6bde276b14862092128bc83e5eaa086"
        },
        "date": 1729852988453,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 76988.79250769495,
            "unit": "iter/sec",
            "range": "stddev: 0.000001948173503267237",
            "extra": "mean: 12.988903545929118 usec\nrounds: 4247"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 56288.075667338206,
            "unit": "iter/sec",
            "range": "stddev: 0.000004727321725486057",
            "extra": "mean: 17.76575212679124 usec\nrounds: 16518"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 77570.40618083245,
            "unit": "iter/sec",
            "range": "stddev: 0.000003485546770941394",
            "extra": "mean: 12.891514293077128 usec\nrounds: 11634"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 47666.83783503424,
            "unit": "iter/sec",
            "range": "stddev: 0.0000049336341497274655",
            "extra": "mean: 20.978945644785746 usec\nrounds: 10336"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 157511.11763149835,
            "unit": "iter/sec",
            "range": "stddev: 9.670365499416323e-7",
            "extra": "mean: 6.348758202195784 usec\nrounds: 26117"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 68735.38763140734,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019405820005139182",
            "extra": "mean: 14.54854674512767 usec\nrounds: 10947"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 90428.04626620907,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016363182711942433",
            "extra": "mean: 11.058516038886019 usec\nrounds: 10547"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58852.50498388887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023032921006713936",
            "extra": "mean: 16.991630182500376 usec\nrounds: 10590"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17259.71608033355,
            "unit": "iter/sec",
            "range": "stddev: 0.000005540170284403407",
            "extra": "mean: 57.93838063995979 usec\nrounds: 6284"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35723.609962589406,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033251572463847885",
            "extra": "mean: 27.992691697373903 usec\nrounds: 8850"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21952.478925838634,
            "unit": "iter/sec",
            "range": "stddev: 0.000004776151172411579",
            "extra": "mean: 45.55294203348371 usec\nrounds: 7722"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15299.76491571867,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057909782902405946",
            "extra": "mean: 65.36048138704538 usec\nrounds: 7338"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12072.69797219127,
            "unit": "iter/sec",
            "range": "stddev: 0.000007101092493024715",
            "extra": "mean: 82.83152633350387 usec\nrounds: 6175"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74806.11261690603,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018116584374502597",
            "extra": "mean: 13.367891540109278 usec\nrounds: 16795"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66497.11598409431,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018901074401359274",
            "extra": "mean: 15.038246173551249 usec\nrounds: 14566"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30360.730917870238,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037757296265936975",
            "extra": "mean: 32.9372834502941 usec\nrounds: 8400"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15257.249201557981,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064239320436420754",
            "extra": "mean: 65.54261431987922 usec\nrounds: 5626"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18338.285541765625,
            "unit": "iter/sec",
            "range": "stddev: 0.000004930691442583189",
            "extra": "mean: 54.530724681022676 usec\nrounds: 7006"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21681.521819481422,
            "unit": "iter/sec",
            "range": "stddev: 0.000004611953332407301",
            "extra": "mean: 46.12222372238989 usec\nrounds: 6192"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 72223.00705063553,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018339258849783548",
            "extra": "mean: 13.84600338364339 usec\nrounds: 17857"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51799.4310260364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021935528331242957",
            "extra": "mean: 19.305231354710468 usec\nrounds: 14752"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 60484.20946392021,
            "unit": "iter/sec",
            "range": "stddev: 0.000001947665351524422",
            "extra": "mean: 16.533240805544725 usec\nrounds: 16497"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 47188.898962680934,
            "unit": "iter/sec",
            "range": "stddev: 0.000002445953255996347",
            "extra": "mean: 21.1914247202683 usec\nrounds: 15542"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40552.216370102855,
            "unit": "iter/sec",
            "range": "stddev: 0.000002712373707556319",
            "extra": "mean: 24.65956461845204 usec\nrounds: 8146"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45096.31948991127,
            "unit": "iter/sec",
            "range": "stddev: 0.000002310859401894431",
            "extra": "mean: 22.174758634653436 usec\nrounds: 12450"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25913.434263469087,
            "unit": "iter/sec",
            "range": "stddev: 0.000005574470250570442",
            "extra": "mean: 38.59002206472219 usec\nrounds: 6412"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23764.630146850704,
            "unit": "iter/sec",
            "range": "stddev: 0.000004410562352461904",
            "extra": "mean: 42.0793420230241 usec\nrounds: 7360"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 115499.42645904492,
            "unit": "iter/sec",
            "range": "stddev: 0.000001246998587944937",
            "extra": "mean: 8.658051651491025 usec\nrounds: 20538"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95042.75562641598,
            "unit": "iter/sec",
            "range": "stddev: 0.000002058888362497182",
            "extra": "mean: 10.521580455123738 usec\nrounds: 23250"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119746.44738657559,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012483848067032207",
            "extra": "mean: 8.35097843672736 usec\nrounds: 16946"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 148633.55729045303,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010342062063588682",
            "extra": "mean: 6.727955774117987 usec\nrounds: 31964"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 136006.67630216343,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010563724937611106",
            "extra": "mean: 7.352580234946108 usec\nrounds: 26492"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 153127.28881854404,
            "unit": "iter/sec",
            "range": "stddev: 9.210560416540949e-7",
            "extra": "mean: 6.530514630772317 usec\nrounds: 22459"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 213199.2837938189,
            "unit": "iter/sec",
            "range": "stddev: 9.008440044702322e-7",
            "extra": "mean: 4.690447276394613 usec\nrounds: 32573"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 106181.266529691,
            "unit": "iter/sec",
            "range": "stddev: 0.000001453258354435002",
            "extra": "mean: 9.4178571482793 usec\nrounds: 17732"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 140818.39134785728,
            "unit": "iter/sec",
            "range": "stddev: 0.000001026677078683908",
            "extra": "mean: 7.101345146954174 usec\nrounds: 25950"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87985.26847443834,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015474917671589081",
            "extra": "mean: 11.365538996911988 usec\nrounds: 13065"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48954.38933305097,
            "unit": "iter/sec",
            "range": "stddev: 0.000002663725879359605",
            "extra": "mean: 20.427177493660654 usec\nrounds: 7523"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 323792.11501241516,
            "unit": "iter/sec",
            "range": "stddev: 6.199480010310662e-7",
            "extra": "mean: 3.0884013341759635 usec\nrounds: 42483"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 280968.4955480629,
            "unit": "iter/sec",
            "range": "stddev: 9.028169051739312e-7",
            "extra": "mean: 3.55911789344702 usec\nrounds: 42854"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 331289.5272529274,
            "unit": "iter/sec",
            "range": "stddev: 6.945058165703587e-7",
            "extra": "mean: 3.018507733377689 usec\nrounds: 46286"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 221961.33781655828,
            "unit": "iter/sec",
            "range": "stddev: 8.161487349853173e-7",
            "extra": "mean: 4.505289118533147 usec\nrounds: 40390"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 341534.5697565715,
            "unit": "iter/sec",
            "range": "stddev: 6.062495063480626e-7",
            "extra": "mean: 2.9279612916278115 usec\nrounds: 59497"
          }
        ]
      },
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
          "id": "ed6dcff2425f43102cec082690cbf741cedd41e0",
          "message": "Merge pull request #74 from amsdal/bugfix/fix-version\n\nFixed core version",
          "timestamp": "2024-10-25T13:48:14+03:00",
          "tree_id": "17bcf6f07bce61fb6c526e47348cf6bd7ab63fed",
          "url": "https://github.com/amsdal/amsdal-glue/commit/ed6dcff2425f43102cec082690cbf741cedd41e0"
        },
        "date": 1729853319035,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 76995.82514064194,
            "unit": "iter/sec",
            "range": "stddev: 0.000001946151468424582",
            "extra": "mean: 12.987717167435797 usec\nrounds: 4423"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 53574.544464326034,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051933169339608846",
            "extra": "mean: 18.665581014242225 usec\nrounds: 16462"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 78976.66153765362,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030761302779044627",
            "extra": "mean: 12.661968492087134 usec\nrounds: 8569"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 48430.25965773136,
            "unit": "iter/sec",
            "range": "stddev: 0.000004275269259393197",
            "extra": "mean: 20.648247749800387 usec\nrounds: 9415"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 150987.11931862956,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014613490991472726",
            "extra": "mean: 6.623081521872674 usec\nrounds: 25778"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 67277.04695113546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019262285248232847",
            "extra": "mean: 14.863910431834473 usec\nrounds: 11745"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 90380.08154189825,
            "unit": "iter/sec",
            "range": "stddev: 0.000001803236366445789",
            "extra": "mean: 11.064384795187662 usec\nrounds: 11127"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57927.72469493077,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024264100956946725",
            "extra": "mean: 17.262891046841162 usec\nrounds: 11852"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17193.198664394266,
            "unit": "iter/sec",
            "range": "stddev: 0.000005006011684978289",
            "extra": "mean: 58.16253389027137 usec\nrounds: 6014"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35073.80764683763,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036867727779742796",
            "extra": "mean: 28.511304220776932 usec\nrounds: 9237"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21463.164440746874,
            "unit": "iter/sec",
            "range": "stddev: 0.000004733579613334672",
            "extra": "mean: 46.5914521952571 usec\nrounds: 7880"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15152.213535721941,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061845718813627495",
            "extra": "mean: 65.9969579786122 usec\nrounds: 6978"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11934.55379813455,
            "unit": "iter/sec",
            "range": "stddev: 0.000007095407868341071",
            "extra": "mean: 83.79031314570862 usec\nrounds: 5841"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 74358.0624845299,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019709381302710303",
            "extra": "mean: 13.448440782168694 usec\nrounds: 16115"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66562.6360017899,
            "unit": "iter/sec",
            "range": "stddev: 0.000002141255419747026",
            "extra": "mean: 15.023443482212897 usec\nrounds: 17573"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 29902.1710994169,
            "unit": "iter/sec",
            "range": "stddev: 0.000004006471356557082",
            "extra": "mean: 33.44238773416357 usec\nrounds: 8181"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15364.068460155268,
            "unit": "iter/sec",
            "range": "stddev: 0.000005567657907917787",
            "extra": "mean: 65.08692685100768 usec\nrounds: 5373"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18044.454985586694,
            "unit": "iter/sec",
            "range": "stddev: 0.000005948210416198136",
            "extra": "mean: 55.418686837522465 usec\nrounds: 7074"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21341.467006380088,
            "unit": "iter/sec",
            "range": "stddev: 0.000004618461615646697",
            "extra": "mean: 46.85713497113612 usec\nrounds: 6695"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 72146.85975052565,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017592240782375694",
            "extra": "mean: 13.860617128144847 usec\nrounds: 18300"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51665.54273225747,
            "unit": "iter/sec",
            "range": "stddev: 0.00000213478820275003",
            "extra": "mean: 19.355259755660096 usec\nrounds: 14890"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 59863.2763857023,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021031374380349883",
            "extra": "mean: 16.70473218934671 usec\nrounds: 16736"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 46631.286352794814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023178308432618846",
            "extra": "mean: 21.44482981735428 usec\nrounds: 15407"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40307.23588602542,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026364246118193814",
            "extra": "mean: 24.80944123352059 usec\nrounds: 8252"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45211.46504063493,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025122866349263644",
            "extra": "mean: 22.118283473035547 usec\nrounds: 12523"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25784.676739658516,
            "unit": "iter/sec",
            "range": "stddev: 0.000004192937401183647",
            "extra": "mean: 38.78272394479682 usec\nrounds: 6437"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23393.207179098827,
            "unit": "iter/sec",
            "range": "stddev: 0.000004435225128723301",
            "extra": "mean: 42.747451956629185 usec\nrounds: 6891"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117999.4748948287,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011500244897793033",
            "extra": "mean: 8.474613983590062 usec\nrounds: 21537"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96682.04593218802,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014181800259222417",
            "extra": "mean: 10.343182028868025 usec\nrounds: 26017"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119829.31177592433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012093725610497387",
            "extra": "mean: 8.345203566469253 usec\nrounds: 17455"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 147032.61640158924,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010344579491617967",
            "extra": "mean: 6.801212033585163 usec\nrounds: 33806"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 133367.77970181793,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010851044250366397",
            "extra": "mean: 7.498062892220204 usec\nrounds: 29557"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 151430.56101750705,
            "unit": "iter/sec",
            "range": "stddev: 0.000001070432206210884",
            "extra": "mean: 6.603686820419221 usec\nrounds: 22846"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 210541.38349888916,
            "unit": "iter/sec",
            "range": "stddev: 8.151469452116556e-7",
            "extra": "mean: 4.749660059136431 usec\nrounds: 33598"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104274.58078448618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013936144233997564",
            "extra": "mean: 9.590064927393874 usec\nrounds: 16284"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 139269.35491628872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010920920094436983",
            "extra": "mean: 7.180330522828045 usec\nrounds: 29350"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 87030.90609883393,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015320402205813574",
            "extra": "mean: 11.490171076288476 usec\nrounds: 13714"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48320.53326183683,
            "unit": "iter/sec",
            "range": "stddev: 0.000002714528363042709",
            "extra": "mean: 20.69513584589912 usec\nrounds: 8763"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 318711.43431091774,
            "unit": "iter/sec",
            "range": "stddev: 6.673137586441595e-7",
            "extra": "mean: 3.1376345256080573 usec\nrounds: 45973"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 279643.78626226675,
            "unit": "iter/sec",
            "range": "stddev: 6.966637152840987e-7",
            "extra": "mean: 3.5759779016228164 usec\nrounds: 42599"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324990.0861089442,
            "unit": "iter/sec",
            "range": "stddev: 6.223570637802988e-7",
            "extra": "mean: 3.07701693910988 usec\nrounds: 46881"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 221780.80571884743,
            "unit": "iter/sec",
            "range": "stddev: 7.96250744815542e-7",
            "extra": "mean: 4.508956475104995 usec\nrounds: 48127"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331537.17690570967,
            "unit": "iter/sec",
            "range": "stddev: 6.41617272738459e-7",
            "extra": "mean: 3.0162529865674865 usec\nrounds: 59127"
          }
        ]
      },
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
          "id": "e1fd5b3050ffb589bfeeb0403462282b36041ccd",
          "message": "Merge pull request #75 from amsdal/feature/async-connections\n\nAsync connections",
          "timestamp": "2024-11-19T12:52:09+02:00",
          "tree_id": "2984c0d40e65261efe0b6c11f9ed88fb5120a94a",
          "url": "https://github.com/amsdal/amsdal-glue/commit/e1fd5b3050ffb589bfeeb0403462282b36041ccd"
        },
        "date": 1732013556300,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 59282.07751580986,
            "unit": "iter/sec",
            "range": "stddev: 0.000005171661793388682",
            "extra": "mean: 16.868504646000492 usec\nrounds: 3399"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59501.055058266094,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028565212423501637",
            "extra": "mean: 16.806424676348264 usec\nrounds: 15604"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 86375.59417564544,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015359813740007521",
            "extra": "mean: 11.577344382332031 usec\nrounds: 12222"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 49776.765274203106,
            "unit": "iter/sec",
            "range": "stddev: 0.000003272928439918711",
            "extra": "mean: 20.0896943481832 usec\nrounds: 10279"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 154944.65943346967,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010551575788167726",
            "extra": "mean: 6.453917183440461 usec\nrounds: 25529"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 65345.6127491752,
            "unit": "iter/sec",
            "range": "stddev: 0.000003042693982404535",
            "extra": "mean: 15.30324620014558 usec\nrounds: 10767"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 88422.0779524473,
            "unit": "iter/sec",
            "range": "stddev: 0.00000215789399968055",
            "extra": "mean: 11.309392667041733 usec\nrounds: 11549"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58796.92254419497,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021870610038918815",
            "extra": "mean: 17.00769286433904 usec\nrounds: 11518"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16986.909775260046,
            "unit": "iter/sec",
            "range": "stddev: 0.000015147326455419528",
            "extra": "mean: 58.868859211603805 usec\nrounds: 5625"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 34895.65279458855,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034743889619504584",
            "extra": "mean: 28.656864678429955 usec\nrounds: 9764"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 20984.222584524,
            "unit": "iter/sec",
            "range": "stddev: 0.000007626225345320128",
            "extra": "mean: 47.65485097062908 usec\nrounds: 7723"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 14943.847160070187,
            "unit": "iter/sec",
            "range": "stddev: 0.000007827826641194039",
            "extra": "mean: 66.91717261884143 usec\nrounds: 6918"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11892.034068789879,
            "unit": "iter/sec",
            "range": "stddev: 0.000007234580532092869",
            "extra": "mean: 84.08990373013278 usec\nrounds: 5887"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73182.61219741721,
            "unit": "iter/sec",
            "range": "stddev: 0.000001836520096727305",
            "extra": "mean: 13.664448015361938 usec\nrounds: 16701"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 64904.55021651988,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020163751559643674",
            "extra": "mean: 15.407240273047519 usec\nrounds: 16682"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30172.047533695957,
            "unit": "iter/sec",
            "range": "stddev: 0.00000383670756176145",
            "extra": "mean: 33.14325946501331 usec\nrounds: 8576"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15246.498720442672,
            "unit": "iter/sec",
            "range": "stddev: 0.00000581013005266864",
            "extra": "mean: 65.58882916896776 usec\nrounds: 4946"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17960.04519601239,
            "unit": "iter/sec",
            "range": "stddev: 0.000005405245287211791",
            "extra": "mean: 55.67914718956425 usec\nrounds: 6056"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21248.06806490903,
            "unit": "iter/sec",
            "range": "stddev: 0.000004752671951594185",
            "extra": "mean: 47.06310225217557 usec\nrounds: 5608"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 71210.4582993008,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018469067238971267",
            "extra": "mean: 14.042881114413763 usec\nrounds: 18317"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 50787.900465224084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022731458772597128",
            "extra": "mean: 19.68972906617253 usec\nrounds: 15210"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 60040.146529145335,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023496101771642523",
            "extra": "mean: 16.655522309802645 usec\nrounds: 16195"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 46243.75338594292,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024746831673570153",
            "extra": "mean: 21.624542273940463 usec\nrounds: 14966"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 39932.21431411709,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025526934105147387",
            "extra": "mean: 25.042437970850862 usec\nrounds: 8131"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45474.26828034816,
            "unit": "iter/sec",
            "range": "stddev: 0.000002371786952041733",
            "extra": "mean: 21.99045829247907 usec\nrounds: 11979"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25547.631235621262,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045137030490256744",
            "extra": "mean: 39.1425721929825 usec\nrounds: 5871"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23195.415949764898,
            "unit": "iter/sec",
            "range": "stddev: 0.000004894367427701049",
            "extra": "mean: 43.11196669918462 usec\nrounds: 8410"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 116031.12203424172,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012253890984208432",
            "extra": "mean: 8.618377401408667 usec\nrounds: 21498"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96008.3846789727,
            "unit": "iter/sec",
            "range": "stddev: 0.00000228730841783882",
            "extra": "mean: 10.415756950226195 usec\nrounds: 24402"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 117778.29315203686,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012860437960839303",
            "extra": "mean: 8.4905288847167 usec\nrounds: 16224"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 147800.01745382507,
            "unit": "iter/sec",
            "range": "stddev: 0.000001061329622528755",
            "extra": "mean: 6.765899065691348 usec\nrounds: 29510"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 135247.41610473828,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010575859301230265",
            "extra": "mean: 7.393856598528878 usec\nrounds: 26582"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 149565.52604733358,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010612789084858376",
            "extra": "mean: 6.6860327137386335 usec\nrounds: 23533"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 206652.4352900271,
            "unit": "iter/sec",
            "range": "stddev: 8.702445041602187e-7",
            "extra": "mean: 4.83904290117146 usec\nrounds: 33092"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103949.05896181108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013100736238623667",
            "extra": "mean: 9.620096708786763 usec\nrounds: 16030"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 139514.44346381328,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011756335890312784",
            "extra": "mean: 7.167716654794786 usec\nrounds: 29341"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86320.64477173856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015932913385986962",
            "extra": "mean: 11.584714208800728 usec\nrounds: 12891"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48427.575224585875,
            "unit": "iter/sec",
            "range": "stddev: 0.000002617603795129565",
            "extra": "mean: 20.649392321677023 usec\nrounds: 8797"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 321960.8900893092,
            "unit": "iter/sec",
            "range": "stddev: 6.288184982017423e-7",
            "extra": "mean: 3.1059673108824133 usec\nrounds: 41966"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 284041.9077553704,
            "unit": "iter/sec",
            "range": "stddev: 7.081892077822481e-7",
            "extra": "mean: 3.5206072508893462 usec\nrounds: 39955"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 324813.5435287469,
            "unit": "iter/sec",
            "range": "stddev: 6.005815840381365e-7",
            "extra": "mean: 3.0786893586273663 usec\nrounds: 41512"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220976.25833598393,
            "unit": "iter/sec",
            "range": "stddev: 7.971640170514079e-7",
            "extra": "mean: 4.525373031158611 usec\nrounds: 43005"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331830.0763523249,
            "unit": "iter/sec",
            "range": "stddev: 5.792595812464742e-7",
            "extra": "mean: 3.0135906033371036 usec\nrounds: 50845"
          }
        ]
      },
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
          "id": "60bd115accf810397158ca8fb3a886f3ca32800e",
          "message": "Merge pull request #76 from amsdal/async-postgres-connection\n\nAsync postgres connection",
          "timestamp": "2024-12-05T14:49:50+02:00",
          "tree_id": "c4d5075c6ce4ac21596f54b7628e1e276c79e09c",
          "url": "https://github.com/amsdal/amsdal-glue/commit/60bd115accf810397158ca8fb3a886f3ca32800e"
        },
        "date": 1733403017394,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 46953.05072587271,
            "unit": "iter/sec",
            "range": "stddev: 0.000004257090251996044",
            "extra": "mean: 21.297870629074296 usec\nrounds: 3846"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 54442.93164065199,
            "unit": "iter/sec",
            "range": "stddev: 0.000004442155492634797",
            "extra": "mean: 18.36785731158735 usec\nrounds: 9453"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 81327.68879746887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025889396819893656",
            "extra": "mean: 12.29593530550597 usec\nrounds: 14706"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 45858.7936051941,
            "unit": "iter/sec",
            "range": "stddev: 0.000004331426477969942",
            "extra": "mean: 21.806068615959777 usec\nrounds: 5962"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 111675.29259137732,
            "unit": "iter/sec",
            "range": "stddev: 0.000003081086023256514",
            "extra": "mean: 8.954532169071856 usec\nrounds: 24429"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 63864.59665111256,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025633284452352365",
            "extra": "mean: 15.658127545421197 usec\nrounds: 11261"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 72580.18700977888,
            "unit": "iter/sec",
            "range": "stddev: 0.000004183749097883981",
            "extra": "mean: 13.777864747927252 usec\nrounds: 10861"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 48685.73937536263,
            "unit": "iter/sec",
            "range": "stddev: 0.000005846265381773109",
            "extra": "mean: 20.539895518276737 usec\nrounds: 7576"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16067.657695475315,
            "unit": "iter/sec",
            "range": "stddev: 0.000015315815154506102",
            "extra": "mean: 62.23682499046529 usec\nrounds: 5823"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 34087.167079942396,
            "unit": "iter/sec",
            "range": "stddev: 0.000003361527578372282",
            "extra": "mean: 29.336553479342115 usec\nrounds: 10696"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 19717.256859146677,
            "unit": "iter/sec",
            "range": "stddev: 0.000011031434633246074",
            "extra": "mean: 50.71699411047172 usec\nrounds: 6440"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 14667.703160924404,
            "unit": "iter/sec",
            "range": "stddev: 0.000005711647085122489",
            "extra": "mean: 68.17700010892345 usec\nrounds: 6764"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11548.364662163694,
            "unit": "iter/sec",
            "range": "stddev: 0.000007843227282203674",
            "extra": "mean: 86.59234699059465 usec\nrounds: 6032"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 71097.34295675022,
            "unit": "iter/sec",
            "range": "stddev: 0.000001853597073952599",
            "extra": "mean: 14.06522323356469 usec\nrounds: 16217"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 62877.40618216965,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022179027772134267",
            "extra": "mean: 15.903963931062622 usec\nrounds: 16530"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 28609.269726980863,
            "unit": "iter/sec",
            "range": "stddev: 0.000004205524076531509",
            "extra": "mean: 34.95370589822916 usec\nrounds: 7424"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 14729.04727444717,
            "unit": "iter/sec",
            "range": "stddev: 0.000007448359515346122",
            "extra": "mean: 67.89305386607454 usec\nrounds: 5498"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17564.236470084328,
            "unit": "iter/sec",
            "range": "stddev: 0.000005636187823192523",
            "extra": "mean: 56.93387251436834 usec\nrounds: 6283"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 20788.704145974625,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047492949950282944",
            "extra": "mean: 48.10304639376153 usec\nrounds: 5586"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 65498.77758366765,
            "unit": "iter/sec",
            "range": "stddev: 0.00011201329990705405",
            "extra": "mean: 15.267460506764534 usec\nrounds: 18389"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 49440.66463303219,
            "unit": "iter/sec",
            "range": "stddev: 0.000002273892176816603",
            "extra": "mean: 20.22626531059783 usec\nrounds: 14639"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 58657.7619017569,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021111035119252333",
            "extra": "mean: 17.048042195589602 usec\nrounds: 16874"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 44946.558045011916,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025566045746187822",
            "extra": "mean: 22.248644690402006 usec\nrounds: 14484"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 38773.148815697474,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029142428076817713",
            "extra": "mean: 25.79104433208029 usec\nrounds: 6622"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 43221.36564703637,
            "unit": "iter/sec",
            "range": "stddev: 0.000002629729142452307",
            "extra": "mean: 23.136705308351786 usec\nrounds: 12467"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 24288.007721651844,
            "unit": "iter/sec",
            "range": "stddev: 0.000005925984928190496",
            "extra": "mean: 41.17258243081575 usec\nrounds: 4811"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 22729.196035042823,
            "unit": "iter/sec",
            "range": "stddev: 0.00000472971708619802",
            "extra": "mean: 43.99627679123565 usec\nrounds: 7804"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 108718.72646189485,
            "unit": "iter/sec",
            "range": "stddev: 0.000002308884621223893",
            "extra": "mean: 9.198047406768445 usec\nrounds: 21103"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 90999.48101660845,
            "unit": "iter/sec",
            "range": "stddev: 0.000001666899205969787",
            "extra": "mean: 10.98907366095295 usec\nrounds: 24860"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 115490.02515375394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012862722025123368",
            "extra": "mean: 8.658756448175348 usec\nrounds: 15996"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 142145.7880581876,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011547153931153394",
            "extra": "mean: 7.035030820544949 usec\nrounds: 29362"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 128291.58279786806,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012317219789400332",
            "extra": "mean: 7.794743647177279 usec\nrounds: 27046"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 144998.3608735932,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010262320027941854",
            "extra": "mean: 6.896629685847145 usec\nrounds: 22930"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 200461.0006462821,
            "unit": "iter/sec",
            "range": "stddev: 8.083786536421583e-7",
            "extra": "mean: 4.988501487950378 usec\nrounds: 34079"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 100488.6277505924,
            "unit": "iter/sec",
            "range": "stddev: 0.000001275424433267235",
            "extra": "mean: 9.951374821058844 usec\nrounds: 16214"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 136492.78903360316,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011703699116439662",
            "extra": "mean: 7.32639436178427 usec\nrounds: 29626"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 85275.43191755304,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014985903345512783",
            "extra": "mean: 11.726706948454174 usec\nrounds: 12508"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 46967.114590859834,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027313139948792725",
            "extra": "mean: 21.291493180094307 usec\nrounds: 8895"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 316680.92644808954,
            "unit": "iter/sec",
            "range": "stddev: 7.100517414472838e-7",
            "extra": "mean: 3.157752540438903 usec\nrounds: 43691"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 256712.65448847838,
            "unit": "iter/sec",
            "range": "stddev: 6.762695403199045e-7",
            "extra": "mean: 3.8954059432425896 usec\nrounds: 37281"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 329369.3131335035,
            "unit": "iter/sec",
            "range": "stddev: 7.609568752768349e-7",
            "extra": "mean: 3.036105551201333 usec\nrounds: 42851"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 211397.8495586711,
            "unit": "iter/sec",
            "range": "stddev: 8.213149916169439e-7",
            "extra": "mean: 4.7304170883841525 usec\nrounds: 39372"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 331859.045623824,
            "unit": "iter/sec",
            "range": "stddev: 6.030644800133988e-7",
            "extra": "mean: 3.013327535249835 usec\nrounds: 54533"
          }
        ]
      },
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
          "id": "d8fc925bb846b3b8c3b508077f5b858373c4ea96",
          "message": "Merge pull request #77 from amsdal/feauture/async-safe-descriptor\n\nAsync safe descriptor",
          "timestamp": "2024-12-18T18:55:12+02:00",
          "tree_id": "d017b7cf62a1da272224472a683ef2200c5b8850",
          "url": "https://github.com/amsdal/amsdal-glue/commit/d8fc925bb846b3b8c3b508077f5b858373c4ea96"
        },
        "date": 1734540940333,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 68993.14109974998,
            "unit": "iter/sec",
            "range": "stddev: 0.000004010847967530306",
            "extra": "mean: 14.494194409183436 usec\nrounds: 4529"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 58981.70378542991,
            "unit": "iter/sec",
            "range": "stddev: 0.000003226916320571874",
            "extra": "mean: 16.954410195370233 usec\nrounds: 12173"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 84346.98199836927,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022188161129641605",
            "extra": "mean: 11.855788746766702 usec\nrounds: 15151"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 43848.73125436191,
            "unit": "iter/sec",
            "range": "stddev: 0.000006552112166493949",
            "extra": "mean: 22.805676957882874 usec\nrounds: 8175"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 97883.82725371902,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032447357123983884",
            "extra": "mean: 10.21619227666648 usec\nrounds: 18109"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 61571.96188822666,
            "unit": "iter/sec",
            "range": "stddev: 0.000004044928376461156",
            "extra": "mean: 16.241158626962847 usec\nrounds: 6910"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 88710.25953478708,
            "unit": "iter/sec",
            "range": "stddev: 0.000001961017729240074",
            "extra": "mean: 11.27265330125494 usec\nrounds: 10659"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 55980.479273896926,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025821140721473274",
            "extra": "mean: 17.8633697490741 usec\nrounds: 11517"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 15218.21170340985,
            "unit": "iter/sec",
            "range": "stddev: 0.00002217145687205882",
            "extra": "mean: 65.7107431207529 usec\nrounds: 5890"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 33474.7949779111,
            "unit": "iter/sec",
            "range": "stddev: 0.00008823676043019055",
            "extra": "mean: 29.873222544301367 usec\nrounds: 8734"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 19567.69135119611,
            "unit": "iter/sec",
            "range": "stddev: 0.000013893318292622116",
            "extra": "mean: 51.10464908977999 usec\nrounds: 6885"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 14560.383542476016,
            "unit": "iter/sec",
            "range": "stddev: 0.000011601031527781536",
            "extra": "mean: 68.6795095117356 usec\nrounds: 7021"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11829.571554816945,
            "unit": "iter/sec",
            "range": "stddev: 0.000007099705223007457",
            "extra": "mean: 84.53391531266446 usec\nrounds: 5746"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73334.66867323082,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021450568532330663",
            "extra": "mean: 13.63611533387929 usec\nrounds: 16077"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 64958.130732578895,
            "unit": "iter/sec",
            "range": "stddev: 0.000002098429511294214",
            "extra": "mean: 15.394531657889337 usec\nrounds: 17786"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30071.851779489178,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036647346275451167",
            "extra": "mean: 33.253688776228294 usec\nrounds: 8239"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15079.148399583735,
            "unit": "iter/sec",
            "range": "stddev: 0.000006309848709085875",
            "extra": "mean: 66.31674239823818 usec\nrounds: 5038"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17937.044817130405,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052874620770311515",
            "extra": "mean: 55.75054364835899 usec\nrounds: 7113"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21167.565518946685,
            "unit": "iter/sec",
            "range": "stddev: 0.000005518852814508403",
            "extra": "mean: 47.24208833107988 usec\nrounds: 6498"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 70896.77475813686,
            "unit": "iter/sec",
            "range": "stddev: 0.000002178568577838227",
            "extra": "mean: 14.105013992688427 usec\nrounds: 18250"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 50381.43928455133,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025489819566015406",
            "extra": "mean: 19.848579441171985 usec\nrounds: 16351"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 59246.305616210106,
            "unit": "iter/sec",
            "range": "stddev: 0.000002157723920899317",
            "extra": "mean: 16.878689558769633 usec\nrounds: 17238"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 45569.89004927876,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028861802701674823",
            "extra": "mean: 21.944314522563285 usec\nrounds: 15370"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40575.98295527765,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029508724083327733",
            "extra": "mean: 24.645120762747453 usec\nrounds: 7144"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45222.766134279926,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024073352793261665",
            "extra": "mean: 22.11275615097716 usec\nrounds: 12482"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25420.936996050397,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045764965125194745",
            "extra": "mean: 39.33765305957715 usec\nrounds: 6786"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23266.484889332674,
            "unit": "iter/sec",
            "range": "stddev: 0.000005486125038589043",
            "extra": "mean: 42.980278488844036 usec\nrounds: 8227"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 116048.72976771412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012894096933245576",
            "extra": "mean: 8.617069760277632 usec\nrounds: 22007"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95297.38376901351,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013230365981923166",
            "extra": "mean: 10.493467506136886 usec\nrounds: 20459"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 119163.10339200658,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011729386631899238",
            "extra": "mean: 8.39185932167557 usec\nrounds: 15830"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 146592.4855408722,
            "unit": "iter/sec",
            "range": "stddev: 0.000001061038220850775",
            "extra": "mean: 6.8216320659982586 usec\nrounds: 30992"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 133831.33817665357,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011543101154086528",
            "extra": "mean: 7.472091466947961 usec\nrounds: 29036"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 148098.16794710312,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010577311150527462",
            "extra": "mean: 6.752277991427783 usec\nrounds: 23002"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 205412.22936966314,
            "unit": "iter/sec",
            "range": "stddev: 9.758865629229724e-7",
            "extra": "mean: 4.868259319655131 usec\nrounds: 34257"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104303.61512033406,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013703303900561248",
            "extra": "mean: 9.587395401840192 usec\nrounds: 16256"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137859.70222136893,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013997436327475392",
            "extra": "mean: 7.253751342029195 usec\nrounds: 30564"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 85749.65218498137,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017173692776418198",
            "extra": "mean: 11.661854882428841 usec\nrounds: 12291"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48847.91281828736,
            "unit": "iter/sec",
            "range": "stddev: 0.000003032308874066013",
            "extra": "mean: 20.471703749553587 usec\nrounds: 8779"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 301758.0527979289,
            "unit": "iter/sec",
            "range": "stddev: 7.159549523885476e-7",
            "extra": "mean: 3.313913218646218 usec\nrounds: 40122"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 276178.45812857733,
            "unit": "iter/sec",
            "range": "stddev: 9.616857638952606e-7",
            "extra": "mean: 3.6208472115317596 usec\nrounds: 39514"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 322616.3743998925,
            "unit": "iter/sec",
            "range": "stddev: 6.30519799489776e-7",
            "extra": "mean: 3.099656680043371 usec\nrounds: 44014"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 219781.1868859163,
            "unit": "iter/sec",
            "range": "stddev: 9.429235826001057e-7",
            "extra": "mean: 4.549979978582418 usec\nrounds: 41564"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 327538.1355134704,
            "unit": "iter/sec",
            "range": "stddev: 7.881114603300851e-7",
            "extra": "mean: 3.053079600738198 usec\nrounds: 54301"
          }
        ]
      },
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
          "id": "2ef702f0c6238c4b86939d6d998b6ef0ab873576",
          "message": "Merge pull request #78 from amsdal/feature/postgres-lock\n\nPostgres select for update",
          "timestamp": "2025-02-06T20:25:32+02:00",
          "tree_id": "24e3e3b6a4951856e698c9146c98ff059bae2add",
          "url": "https://github.com/amsdal/amsdal-glue/commit/2ef702f0c6238c4b86939d6d998b6ef0ab873576"
        },
        "date": 1738866362278,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 78309.98387293138,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020046946841888086",
            "extra": "mean: 12.769763835255494 usec\nrounds: 4554"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59224.98157996047,
            "unit": "iter/sec",
            "range": "stddev: 0.000004748245038559348",
            "extra": "mean: 16.884766754209725 usec\nrounds: 16635"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 85080.56387815895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023418945133160804",
            "extra": "mean: 11.753565731323393 usec\nrounds: 17126"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 42005.45854646454,
            "unit": "iter/sec",
            "range": "stddev: 0.000007122810869051856",
            "extra": "mean: 23.80642979754274 usec\nrounds: 11760"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 160880.6427039541,
            "unit": "iter/sec",
            "range": "stddev: 8.302525193603656e-7",
            "extra": "mean: 6.215788196720215 usec\nrounds: 32091"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 70093.43776735183,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018086216179357729",
            "extra": "mean: 14.266670773362764 usec\nrounds: 17404"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 92579.97834954485,
            "unit": "iter/sec",
            "range": "stddev: 0.000001756414070744292",
            "extra": "mean: 10.801471525780675 usec\nrounds: 13556"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58505.22007449464,
            "unit": "iter/sec",
            "range": "stddev: 0.000005060290505099908",
            "extra": "mean: 17.092491896051346 usec\nrounds: 15462"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16713.705617088264,
            "unit": "iter/sec",
            "range": "stddev: 0.00001854559229403534",
            "extra": "mean: 59.83113636856148 usec\nrounds: 7442"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35153.44363016472,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053212576873344845",
            "extra": "mean: 28.44671522143318 usec\nrounds: 10671"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22357.888471942086,
            "unit": "iter/sec",
            "range": "stddev: 0.000004262892221954175",
            "extra": "mean: 44.72694285307599 usec\nrounds: 9149"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15762.014517925847,
            "unit": "iter/sec",
            "range": "stddev: 0.000004784674793491905",
            "extra": "mean: 63.44366697941551 usec\nrounds: 8239"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12497.397565736632,
            "unit": "iter/sec",
            "range": "stddev: 0.000004529058816046456",
            "extra": "mean: 80.01665904761167 usec\nrounds: 6807"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 76542.21994470956,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015041466673716962",
            "extra": "mean: 13.064685094348611 usec\nrounds: 15040"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68617.21384559742,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016816406682829474",
            "extra": "mean: 14.573602511028819 usec\nrounds: 19320"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 31384.88768162023,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035563011190505015",
            "extra": "mean: 31.86246865511725 usec\nrounds: 10029"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16044.168055296957,
            "unit": "iter/sec",
            "range": "stddev: 0.000004819272882996036",
            "extra": "mean: 62.32794349656862 usec\nrounds: 5913"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19051.57589617469,
            "unit": "iter/sec",
            "range": "stddev: 0.000004084507831254223",
            "extra": "mean: 52.489096201264225 usec\nrounds: 8096"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22462.535671925343,
            "unit": "iter/sec",
            "range": "stddev: 0.000004222515193480976",
            "extra": "mean: 44.518571482997956 usec\nrounds: 8108"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 74856.51064975878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014985530212486741",
            "extra": "mean: 13.358891448718929 usec\nrounds: 21242"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 53232.34434380653,
            "unit": "iter/sec",
            "range": "stddev: 0.000002150330949255359",
            "extra": "mean: 18.78557129743146 usec\nrounds: 18093"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 62170.198607186314,
            "unit": "iter/sec",
            "range": "stddev: 0.000001652055279002346",
            "extra": "mean: 16.084877037603817 usec\nrounds: 18621"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 48360.02429983562,
            "unit": "iter/sec",
            "range": "stddev: 0.000001975866870390612",
            "extra": "mean: 20.678236094339578 usec\nrounds: 19657"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 42216.49603255124,
            "unit": "iter/sec",
            "range": "stddev: 0.000002018433896046167",
            "extra": "mean: 23.68742302129824 usec\nrounds: 8552"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46947.80462067735,
            "unit": "iter/sec",
            "range": "stddev: 0.000001947859803240203",
            "extra": "mean: 21.300250524591455 usec\nrounds: 14660"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26660.34312887245,
            "unit": "iter/sec",
            "range": "stddev: 0.000004413392332904984",
            "extra": "mean: 37.5088945842196 usec\nrounds: 6155"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24488.537661285467,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035440591740599606",
            "extra": "mean: 40.835431410056174 usec\nrounds: 9240"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 121546.78057930889,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013744054325434107",
            "extra": "mean: 8.227284961673693 usec\nrounds: 25850"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99223.16913334973,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011078138126713892",
            "extra": "mean: 10.078291277474342 usec\nrounds: 29520"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 122773.8794371578,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010319038857467915",
            "extra": "mean: 8.145054995283855 usec\nrounds: 21562"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 152871.50797441075,
            "unit": "iter/sec",
            "range": "stddev: 8.551737188446372e-7",
            "extra": "mean: 6.541441327100604 usec\nrounds: 39191"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 140451.30197146945,
            "unit": "iter/sec",
            "range": "stddev: 8.802850009647865e-7",
            "extra": "mean: 7.1199055185913105 usec\nrounds: 25544"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 155083.23185603064,
            "unit": "iter/sec",
            "range": "stddev: 8.553709009866844e-7",
            "extra": "mean: 6.44815037726539 usec\nrounds: 21597"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 208917.50123628782,
            "unit": "iter/sec",
            "range": "stddev: 7.200555943974504e-7",
            "extra": "mean: 4.786578405745863 usec\nrounds: 44064"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 108396.35471194093,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013078753106788448",
            "extra": "mean: 9.22540248385161 usec\nrounds: 19178"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 144348.68539464998,
            "unit": "iter/sec",
            "range": "stddev: 9.402782100666889e-7",
            "extra": "mean: 6.927669602712317 usec\nrounds: 36527"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 90191.66706974398,
            "unit": "iter/sec",
            "range": "stddev: 0.000001248963955128247",
            "extra": "mean: 11.087498795500847 usec\nrounds: 16064"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51841.0705552733,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020772163617005146",
            "extra": "mean: 19.289725101911106 usec\nrounds: 10855"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 325014.5633533378,
            "unit": "iter/sec",
            "range": "stddev: 6.226675833498227e-7",
            "extra": "mean: 3.0767852051997293 usec\nrounds: 48954"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 285454.98653184326,
            "unit": "iter/sec",
            "range": "stddev: 5.885936637662666e-7",
            "extra": "mean: 3.503179300349855 usec\nrounds: 56999"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 335752.78104756156,
            "unit": "iter/sec",
            "range": "stddev: 5.378625069579996e-7",
            "extra": "mean: 2.9783818822883954 usec\nrounds: 62297"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 225887.46775630806,
            "unit": "iter/sec",
            "range": "stddev: 7.875662497316771e-7",
            "extra": "mean: 4.426983089999575 usec\nrounds: 66535"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 343079.2456786538,
            "unit": "iter/sec",
            "range": "stddev: 5.606114175454183e-7",
            "extra": "mean: 2.914778473474472 usec\nrounds: 75808"
          }
        ]
      },
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
          "id": "f48ae1455198ee0a30766e6aaa48815450b230ac",
          "message": "Merge pull request #79 from amsdal/feature/update-actions\n\nUpdate actions",
          "timestamp": "2025-02-06T20:52:14+02:00",
          "tree_id": "461db6a0f1ae82bc5de3fcf4003d13f7e4adc7a1",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f48ae1455198ee0a30766e6aaa48815450b230ac"
        },
        "date": 1738867962913,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 78551.75524366864,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018298499278760229",
            "extra": "mean: 12.730460279315034 usec\nrounds: 5065"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 56630.85219916209,
            "unit": "iter/sec",
            "range": "stddev: 0.000004613554846981244",
            "extra": "mean: 17.65821917147127 usec\nrounds: 16805"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 60629.37331366824,
            "unit": "iter/sec",
            "range": "stddev: 0.000003964960333892761",
            "extra": "mean: 16.493655555805663 usec\nrounds: 18726"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 34407.040604802976,
            "unit": "iter/sec",
            "range": "stddev: 0.0000075600142534766165",
            "extra": "mean: 29.06381898652473 usec\nrounds: 8366"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 159622.33360792216,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010081039095037608",
            "extra": "mean: 6.26478749807207 usec\nrounds: 30860"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 69424.09634926183,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019623400668377928",
            "extra": "mean: 14.404220617711111 usec\nrounds: 16488"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 93310.37361520615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013884365690731295",
            "extra": "mean: 10.71692204474291 usec\nrounds: 10722"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 60810.68079954655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016748883470626434",
            "extra": "mean: 16.444479602133587 usec\nrounds: 14587"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17438.710569236366,
            "unit": "iter/sec",
            "range": "stddev: 0.000014021927042521641",
            "extra": "mean: 57.343689261297804 usec\nrounds: 7559"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36093.62236753134,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027156956091174226",
            "extra": "mean: 27.705725676887663 usec\nrounds: 12079"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22326.51972363749,
            "unit": "iter/sec",
            "range": "stddev: 0.000003995670255423879",
            "extra": "mean: 44.789784183930905 usec\nrounds: 8887"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15655.650099551287,
            "unit": "iter/sec",
            "range": "stddev: 0.000004687173137183413",
            "extra": "mean: 63.874702975679135 usec\nrounds: 7944"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12319.003627861524,
            "unit": "iter/sec",
            "range": "stddev: 0.0000044654484153567224",
            "extra": "mean: 81.17539617719811 usec\nrounds: 4333"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 75861.57251786446,
            "unit": "iter/sec",
            "range": "stddev: 0.000001947474702815334",
            "extra": "mean: 13.181904445290959 usec\nrounds: 13623"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68077.39373894906,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017465679021966554",
            "extra": "mean: 14.689163980551607 usec\nrounds: 21021"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 31352.261826229293,
            "unit": "iter/sec",
            "range": "stddev: 0.000002790746440263915",
            "extra": "mean: 31.89562544299117 usec\nrounds: 10692"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15787.782238738755,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056465195998655445",
            "extra": "mean: 63.34011863593372 usec\nrounds: 6536"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18682.470332616453,
            "unit": "iter/sec",
            "range": "stddev: 0.000004289157601126179",
            "extra": "mean: 53.52611202888775 usec\nrounds: 8203"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22026.265146973747,
            "unit": "iter/sec",
            "range": "stddev: 0.000003541450807394009",
            "extra": "mean: 45.400343332259986 usec\nrounds: 7775"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 73843.18938178274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015588052057799682",
            "extra": "mean: 13.54221030229095 usec\nrounds: 20473"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 52961.341091244365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018559018058753132",
            "extra": "mean: 18.881697090659987 usec\nrounds: 17444"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 61370.937750420984,
            "unit": "iter/sec",
            "range": "stddev: 0.000001639187570490795",
            "extra": "mean: 16.294357503004594 usec\nrounds: 19236"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 47893.697465576915,
            "unit": "iter/sec",
            "range": "stddev: 0.000001993006264862331",
            "extra": "mean: 20.879573992355454 usec\nrounds: 17038"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 42152.13038169394,
            "unit": "iter/sec",
            "range": "stddev: 0.000002069481564239887",
            "extra": "mean: 23.723593349727476 usec\nrounds: 8614"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46531.30234202855,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023081891077772245",
            "extra": "mean: 21.490909337750647 usec\nrounds: 12559"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26782.431052139407,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035333340771129954",
            "extra": "mean: 37.337909992308894 usec\nrounds: 8542"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24149.137100218035,
            "unit": "iter/sec",
            "range": "stddev: 0.000005101163069168099",
            "extra": "mean: 41.40934708557232 usec\nrounds: 6292"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 121806.33991600567,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010202834454186771",
            "extra": "mean: 8.209753291081341 usec\nrounds: 25953"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99714.44926964655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011519584976204824",
            "extra": "mean: 10.028636845757557 usec\nrounds: 29541"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 122919.62024016205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011382436021636554",
            "extra": "mean: 8.135397734276971 usec\nrounds: 22140"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 153879.3860089081,
            "unit": "iter/sec",
            "range": "stddev: 8.649166674300639e-7",
            "extra": "mean: 6.498596244347568 usec\nrounds: 37203"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 138301.48423818388,
            "unit": "iter/sec",
            "range": "stddev: 9.687666298435685e-7",
            "extra": "mean: 7.2305803911532305 usec\nrounds: 39074"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 155966.8975937689,
            "unit": "iter/sec",
            "range": "stddev: 8.358707716210761e-7",
            "extra": "mean: 6.411616922743429 usec\nrounds: 32095"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 216349.13783286925,
            "unit": "iter/sec",
            "range": "stddev: 8.180617898483909e-7",
            "extra": "mean: 4.62215847040955 usec\nrounds: 40889"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 109087.05249508876,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011819523501747518",
            "extra": "mean: 9.166990739299893 usec\nrounds: 23655"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 145087.71674704825,
            "unit": "iter/sec",
            "range": "stddev: 9.40276600509334e-7",
            "extra": "mean: 6.892382225184783 usec\nrounds: 38472"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 89150.32121278932,
            "unit": "iter/sec",
            "range": "stddev: 0.000001295502399616236",
            "extra": "mean: 11.217009500315093 usec\nrounds: 15339"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 50087.63336410882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023180580948159317",
            "extra": "mean: 19.965007983718547 usec\nrounds: 10292"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 328721.88696088037,
            "unit": "iter/sec",
            "range": "stddev: 5.818443799981101e-7",
            "extra": "mean: 3.042085238817716 usec\nrounds: 57090"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 289307.83295373496,
            "unit": "iter/sec",
            "range": "stddev: 5.800520415055931e-7",
            "extra": "mean: 3.4565258388974085 usec\nrounds: 60664"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 335562.161209349,
            "unit": "iter/sec",
            "range": "stddev: 5.35416521967225e-7",
            "extra": "mean: 2.9800737854233947 usec\nrounds: 61456"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 228159.15727182615,
            "unit": "iter/sec",
            "range": "stddev: 7.297521802654476e-7",
            "extra": "mean: 4.382905389191159 usec\nrounds: 63385"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 343272.43555544416,
            "unit": "iter/sec",
            "range": "stddev: 5.525957872972456e-7",
            "extra": "mean: 2.9131380688400292 usec\nrounds: 88769"
          }
        ]
      },
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
          "id": "af79b2b8e5c891c2fc1e8c6073d3ccab02d6a580",
          "message": "Merge pull request #80 from amsdal/bugfix/connections-release\n\nFix connections release",
          "timestamp": "2025-02-06T21:01:27+02:00",
          "tree_id": "14c134beb9977d931701cfa1149a7037fb54d479",
          "url": "https://github.com/amsdal/amsdal-glue/commit/af79b2b8e5c891c2fc1e8c6073d3ccab02d6a580"
        },
        "date": 1738868516106,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 49460.20441777494,
            "unit": "iter/sec",
            "range": "stddev: 0.000004491453846036494",
            "extra": "mean: 20.218274707344747 usec\nrounds: 4021"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 53161.34911403793,
            "unit": "iter/sec",
            "range": "stddev: 0.000005598566109243973",
            "extra": "mean: 18.810658808806213 usec\nrounds: 10809"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 87263.8956436108,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015359672407996617",
            "extra": "mean: 11.45949298532396 usec\nrounds: 19214"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 51511.89372575787,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028175688335649386",
            "extra": "mean: 19.41299237267145 usec\nrounds: 12775"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 128711.83519933533,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024435153179314186",
            "extra": "mean: 7.76929330897431 usec\nrounds: 31789"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 61835.3030112812,
            "unit": "iter/sec",
            "range": "stddev: 0.000004228302525595485",
            "extra": "mean: 16.171991585738013 usec\nrounds: 11579"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 78952.67798370915,
            "unit": "iter/sec",
            "range": "stddev: 0.000003671868108192297",
            "extra": "mean: 12.665814834125538 usec\nrounds: 13966"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 60203.25481298301,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019638262996136046",
            "extra": "mean: 16.610397612328878 usec\nrounds: 15587"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17517.937920749566,
            "unit": "iter/sec",
            "range": "stddev: 0.000013924754835416002",
            "extra": "mean: 57.084344317462424 usec\nrounds: 7460"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 36137.05658590398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029421594236752164",
            "extra": "mean: 27.672425329462808 usec\nrounds: 13400"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21991.29656781563,
            "unit": "iter/sec",
            "range": "stddev: 0.000004588889952422656",
            "extra": "mean: 45.472534869249365 usec\nrounds: 9256"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15466.352659468477,
            "unit": "iter/sec",
            "range": "stddev: 0.0000049123580370697226",
            "extra": "mean: 64.65648508200812 usec\nrounds: 5271"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12188.249803156634,
            "unit": "iter/sec",
            "range": "stddev: 0.000005623034274667",
            "extra": "mean: 82.04623437739274 usec\nrounds: 4128"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 75894.11332207297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017257085083626961",
            "extra": "mean: 13.176252494792124 usec\nrounds: 18797"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68256.89073539518,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016170210909023605",
            "extra": "mean: 14.650535487715112 usec\nrounds: 19198"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30922.180337915474,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029353011248637126",
            "extra": "mean: 32.33924610334939 usec\nrounds: 10931"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15804.882903266925,
            "unit": "iter/sec",
            "range": "stddev: 0.000004425732564119739",
            "extra": "mean: 63.27158550433148 usec\nrounds: 6763"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18826.07596070932,
            "unit": "iter/sec",
            "range": "stddev: 0.000004714321582803698",
            "extra": "mean: 53.117813934621054 usec\nrounds: 8360"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22201.321198557554,
            "unit": "iter/sec",
            "range": "stddev: 0.000004267642115792625",
            "extra": "mean: 45.042364418608166 usec\nrounds: 8218"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 74229.7634078091,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014454179829801473",
            "extra": "mean: 13.471685131287892 usec\nrounds: 22762"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 53953.35770489645,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017818394289505674",
            "extra": "mean: 18.53452764644612 usec\nrounds: 17555"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 62258.54497514961,
            "unit": "iter/sec",
            "range": "stddev: 0.000001717076773974439",
            "extra": "mean: 16.06205221145384 usec\nrounds: 19375"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 48174.28132305827,
            "unit": "iter/sec",
            "range": "stddev: 0.000001886615605337944",
            "extra": "mean: 20.757964053349713 usec\nrounds: 17249"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 42207.323671535654,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021281592049322127",
            "extra": "mean: 23.692570696549364 usec\nrounds: 9178"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 47064.066875512086,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021391336019392492",
            "extra": "mean: 21.247632565308763 usec\nrounds: 15644"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26590.998051218387,
            "unit": "iter/sec",
            "range": "stddev: 0.000004860043990742215",
            "extra": "mean: 37.606711792985166 usec\nrounds: 7886"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24239.93284222864,
            "unit": "iter/sec",
            "range": "stddev: 0.000005222041390527811",
            "extra": "mean: 41.254239708861306 usec\nrounds: 5554"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 120175.25279271012,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010293610595269497",
            "extra": "mean: 8.321180748626313 usec\nrounds: 25349"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99252.24087477574,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013203273461764113",
            "extra": "mean: 10.075339268779603 usec\nrounds: 29467"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 124286.99044584438,
            "unit": "iter/sec",
            "range": "stddev: 9.973256055638736e-7",
            "extra": "mean: 8.045894396612093 usec\nrounds: 22754"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 151841.7847616653,
            "unit": "iter/sec",
            "range": "stddev: 8.60788465795354e-7",
            "extra": "mean: 6.585802462541028 usec\nrounds: 38647"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 139019.8280720522,
            "unit": "iter/sec",
            "range": "stddev: 8.938097511024264e-7",
            "extra": "mean: 7.19321850608039 usec\nrounds: 36112"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 155260.00965451493,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010000951960805773",
            "extra": "mean: 6.440808565098013 usec\nrounds: 31860"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 208860.282131307,
            "unit": "iter/sec",
            "range": "stddev: 7.435591230270426e-7",
            "extra": "mean: 4.787889730855177 usec\nrounds: 46795"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 107868.07478464967,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010692622442149663",
            "extra": "mean: 9.270583553070944 usec\nrounds: 23620"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 142858.59806324972,
            "unit": "iter/sec",
            "range": "stddev: 9.130241455780752e-7",
            "extra": "mean: 6.999928695627101 usec\nrounds: 37623"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88691.06860099766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015533172453697875",
            "extra": "mean: 11.275092472938715 usec\nrounds: 15551"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 49848.92562255784,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026699352557575017",
            "extra": "mean: 20.060612892075568 usec\nrounds: 10751"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 325882.8858913798,
            "unit": "iter/sec",
            "range": "stddev: 6.741297111806971e-7",
            "extra": "mean: 3.0685870393737416 usec\nrounds: 52337"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 285615.42889853445,
            "unit": "iter/sec",
            "range": "stddev: 6.964943249752175e-7",
            "extra": "mean: 3.501211415141205 usec\nrounds: 64903"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 335606.8887860371,
            "unit": "iter/sec",
            "range": "stddev: 5.872231710462204e-7",
            "extra": "mean: 2.9796766199204576 usec\nrounds: 59317"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 227670.03258322342,
            "unit": "iter/sec",
            "range": "stddev: 6.916652766560004e-7",
            "extra": "mean: 4.392321592146546 usec\nrounds: 56573"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 340399.6274034594,
            "unit": "iter/sec",
            "range": "stddev: 5.43454591581866e-7",
            "extra": "mean: 2.9377235446111336 usec\nrounds: 87439"
          }
        ]
      },
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
          "id": "d9ce0db4673b4536e5df1f62d7f2d78a2e6ec853",
          "message": "Merge pull request #81 from amsdal/feature/disable-sqlite-locking\n\nDisable SQLite locking",
          "timestamp": "2025-02-13T20:14:05+02:00",
          "tree_id": "fccccd1b1ea32e7f9cb287819eeff317329fd3b0",
          "url": "https://github.com/amsdal/amsdal-glue/commit/d9ce0db4673b4536e5df1f62d7f2d78a2e6ec853"
        },
        "date": 1739470471079,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 72688.06059751999,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020545995702553153",
            "extra": "mean: 13.757417542573952 usec\nrounds: 4286"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 38125.10375822132,
            "unit": "iter/sec",
            "range": "stddev: 0.000006404210172053889",
            "extra": "mean: 26.229436812597772 usec\nrounds: 11282"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 81232.81206120965,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017591604934040237",
            "extra": "mean: 12.310296475351501 usec\nrounds: 15463"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 47962.08096493794,
            "unit": "iter/sec",
            "range": "stddev: 0.000002591099024214415",
            "extra": "mean: 20.849804259557402 usec\nrounds: 10298"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 144768.4480227695,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013884910360481648",
            "extra": "mean: 6.9075825130260275 usec\nrounds: 18464"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 55784.88475735856,
            "unit": "iter/sec",
            "range": "stddev: 0.000004836682324751682",
            "extra": "mean: 17.926002793580935 usec\nrounds: 12131"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 68370.21748352927,
            "unit": "iter/sec",
            "range": "stddev: 0.000004330242499684206",
            "extra": "mean: 14.626251558156957 usec\nrounds: 11694"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 53846.741495288166,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031379752685000657",
            "extra": "mean: 18.57122589465334 usec\nrounds: 8952"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 15029.21839862481,
            "unit": "iter/sec",
            "range": "stddev: 0.000019672167160139718",
            "extra": "mean: 66.53705957799517 usec\nrounds: 5836"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 33214.4648060318,
            "unit": "iter/sec",
            "range": "stddev: 0.000003451292561398995",
            "extra": "mean: 30.107364542523005 usec\nrounds: 10775"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 20352.343635675028,
            "unit": "iter/sec",
            "range": "stddev: 0.000004990680790618792",
            "extra": "mean: 49.134390510541955 usec\nrounds: 7962"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 14127.822656554312,
            "unit": "iter/sec",
            "range": "stddev: 0.000006105404802405264",
            "extra": "mean: 70.78231545722798 usec\nrounds: 4593"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11108.831440724456,
            "unit": "iter/sec",
            "range": "stddev: 0.000009395881222490663",
            "extra": "mean: 90.01846911944733 usec\nrounds: 5907"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 68597.16231112918,
            "unit": "iter/sec",
            "range": "stddev: 0.000001938128772934035",
            "extra": "mean: 14.577862499098748 usec\nrounds: 18065"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 60825.40166058071,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020782050097574513",
            "extra": "mean: 16.440499736939227 usec\nrounds: 15816"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 28000.88152619984,
            "unit": "iter/sec",
            "range": "stddev: 0.000004158848612436692",
            "extra": "mean: 35.71316135402098 usec\nrounds: 7267"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 14264.723180307456,
            "unit": "iter/sec",
            "range": "stddev: 0.000005974560051697015",
            "extra": "mean: 70.10300777378608 usec\nrounds: 5408"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 16868.84633447037,
            "unit": "iter/sec",
            "range": "stddev: 0.000005973386719498869",
            "extra": "mean: 59.28087672223122 usec\nrounds: 6291"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 20035.27465879871,
            "unit": "iter/sec",
            "range": "stddev: 0.000005586273837233976",
            "extra": "mean: 49.911968616853436 usec\nrounds: 6772"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 66864.2538665694,
            "unit": "iter/sec",
            "range": "stddev: 0.000001812887282027962",
            "extra": "mean: 14.955674253025311 usec\nrounds: 18861"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 48042.82733849478,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023058055487865487",
            "extra": "mean: 20.814761649107616 usec\nrounds: 15513"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 55978.16493731861,
            "unit": "iter/sec",
            "range": "stddev: 0.000002132492606318887",
            "extra": "mean: 17.864108284359574 usec\nrounds: 17621"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 43213.48246040562,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024779033003910033",
            "extra": "mean: 23.14092600419905 usec\nrounds: 15083"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 37679.5881322607,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026576760864053856",
            "extra": "mean: 26.53956822696305 usec\nrounds: 5987"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 42119.19206859354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026550251992948535",
            "extra": "mean: 23.74214582206235 usec\nrounds: 12454"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 23923.167115680277,
            "unit": "iter/sec",
            "range": "stddev: 0.000005008839016232164",
            "extra": "mean: 41.8004854944376 usec\nrounds: 6571"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 21766.819185191307,
            "unit": "iter/sec",
            "range": "stddev: 0.000005994502939547955",
            "extra": "mean: 45.94148513349774 usec\nrounds: 8043"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 107773.4004191256,
            "unit": "iter/sec",
            "range": "stddev: 0.000001373142223029407",
            "extra": "mean: 9.278727367894563 usec\nrounds: 17520"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 89824.9248054516,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014909042775463536",
            "extra": "mean: 11.132767460321977 usec\nrounds: 25273"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 112050.83135863628,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012458428973008344",
            "extra": "mean: 8.924521022064914 usec\nrounds: 16048"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 139529.68678113425,
            "unit": "iter/sec",
            "range": "stddev: 9.928871843949886e-7",
            "extra": "mean: 7.166933597210723 usec\nrounds: 20818"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 127684.83415002533,
            "unit": "iter/sec",
            "range": "stddev: 0.000001083794900141112",
            "extra": "mean: 7.8317836778096455 usec\nrounds: 28171"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 144878.90495199925,
            "unit": "iter/sec",
            "range": "stddev: 9.994184652504053e-7",
            "extra": "mean: 6.902316112420343 usec\nrounds: 26819"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 199317.90053490447,
            "unit": "iter/sec",
            "range": "stddev: 9.779259247981346e-7",
            "extra": "mean: 5.017110843112058 usec\nrounds: 34533"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 99298.65559551114,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013340574698231789",
            "extra": "mean: 10.070629798589191 usec\nrounds: 17203"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 131851.8697521451,
            "unit": "iter/sec",
            "range": "stddev: 0.000001053507453591662",
            "extra": "mean: 7.584268633276101 usec\nrounds: 30289"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 80783.61402631101,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015938026267055932",
            "extra": "mean: 12.378747993055901 usec\nrounds: 12593"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 45434.287542355254,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027298452723492728",
            "extra": "mean: 22.009809201206664 usec\nrounds: 9150"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 298852.5556056098,
            "unit": "iter/sec",
            "range": "stddev: 8.32394256065599e-7",
            "extra": "mean: 3.3461316667463326 usec\nrounds: 43602"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 259953.90205314296,
            "unit": "iter/sec",
            "range": "stddev: 7.72072011408961e-7",
            "extra": "mean: 3.8468358893707535 usec\nrounds: 40713"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 310284.6779595859,
            "unit": "iter/sec",
            "range": "stddev: 6.443548088813168e-7",
            "extra": "mean: 3.222846859780322 usec\nrounds: 49582"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 210875.36993205638,
            "unit": "iter/sec",
            "range": "stddev: 8.06567578710317e-7",
            "extra": "mean: 4.742137501986117 usec\nrounds: 41618"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 312486.0498827952,
            "unit": "iter/sec",
            "range": "stddev: 6.606689206386692e-7",
            "extra": "mean: 3.200142855577304 usec\nrounds: 58997"
          }
        ]
      },
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
          "id": "d393a60e4e7e54940dbc2ab7d173bc4415610fb8",
          "message": "Merge pull request #82 from amsdal/feature/python-classes\n\nChange builder helpers and conditions",
          "timestamp": "2025-02-24T03:06:56+02:00",
          "tree_id": "b6794212592cedf3b69f37122909888e17afd37f",
          "url": "https://github.com/amsdal/amsdal-glue/commit/d393a60e4e7e54940dbc2ab7d173bc4415610fb8"
        },
        "date": 1740359265637,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 73456.5660327935,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018616444834456422",
            "extra": "mean: 13.613486908080704 usec\nrounds: 4513"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 53571.48433510584,
            "unit": "iter/sec",
            "range": "stddev: 0.000003156543115686479",
            "extra": "mean: 18.666647236143348 usec\nrounds: 9684"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 79816.6755645903,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016078397135847844",
            "extra": "mean: 12.528710234126038 usec\nrounds: 13396"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 46139.98222900164,
            "unit": "iter/sec",
            "range": "stddev: 0.000002792684582813712",
            "extra": "mean: 21.673176964759264 usec\nrounds: 8445"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 152542.90672841202,
            "unit": "iter/sec",
            "range": "stddev: 0.000001167954284493974",
            "extra": "mean: 6.555532613393843 usec\nrounds: 22337"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 62935.24032501205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023001993141000874",
            "extra": "mean: 15.88934903300234 usec\nrounds: 8377"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 86194.922618113,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018902454635968135",
            "extra": "mean: 11.601611436331401 usec\nrounds: 8765"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 49673.00884918724,
            "unit": "iter/sec",
            "range": "stddev: 0.000005406129976521451",
            "extra": "mean: 20.13165747692295 usec\nrounds: 10384"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 16104.892710877039,
            "unit": "iter/sec",
            "range": "stddev: 0.000014179257406981629",
            "extra": "mean: 62.09293150550533 usec\nrounds: 5430"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 33533.14828484529,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035661082131182162",
            "extra": "mean: 29.821238122515695 usec\nrounds: 10315"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 17554.649400874063,
            "unit": "iter/sec",
            "range": "stddev: 0.000017422170708998038",
            "extra": "mean: 56.96496564324486 usec\nrounds: 7236"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 11179.2767330117,
            "unit": "iter/sec",
            "range": "stddev: 0.000029015235661072626",
            "extra": "mean: 89.45122514474153 usec\nrounds: 4666"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 10217.825652804513,
            "unit": "iter/sec",
            "range": "stddev: 0.00002537690950694064",
            "extra": "mean: 97.86817998069164 usec\nrounds: 6117"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 72597.1470381427,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020779483750991307",
            "extra": "mean: 13.774645985393857 usec\nrounds: 15816"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 65045.6971993064,
            "unit": "iter/sec",
            "range": "stddev: 0.000002201808798324575",
            "extra": "mean: 15.373807078059318 usec\nrounds: 12999"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 28835.037771872656,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038125541251363093",
            "extra": "mean: 34.680030867705575 usec\nrounds: 7505"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 14637.065067976828,
            "unit": "iter/sec",
            "range": "stddev: 0.000007825269933093041",
            "extra": "mean: 68.31970721970853 usec\nrounds: 5195"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17392.593741957593,
            "unit": "iter/sec",
            "range": "stddev: 0.000005860802466848189",
            "extra": "mean: 57.49573725669318 usec\nrounds: 6755"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 20322.2447250096,
            "unit": "iter/sec",
            "range": "stddev: 0.000005307979041086249",
            "extra": "mean: 49.20716257143328 usec\nrounds: 6657"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 69687.82804946015,
            "unit": "iter/sec",
            "range": "stddev: 0.000001875007086119947",
            "extra": "mean: 14.349708234417369 usec\nrounds: 16900"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 49244.336690504264,
            "unit": "iter/sec",
            "range": "stddev: 0.000002552150815085751",
            "extra": "mean: 20.306903640207402 usec\nrounds: 16484"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 58333.8236412896,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020303022198416564",
            "extra": "mean: 17.142713053566823 usec\nrounds: 16406"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 44641.04054420029,
            "unit": "iter/sec",
            "range": "stddev: 0.000002792118038724032",
            "extra": "mean: 22.400911533634016 usec\nrounds: 10568"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 38731.73479066059,
            "unit": "iter/sec",
            "range": "stddev: 0.0000043966144997864165",
            "extra": "mean: 25.818621484548913 usec\nrounds: 7131"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44389.97425264223,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026853343478838684",
            "extra": "mean: 22.527609372075204 usec\nrounds: 13085"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 24397.71928316173,
            "unit": "iter/sec",
            "range": "stddev: 0.000004740442981414042",
            "extra": "mean: 40.98743773522132 usec\nrounds: 5823"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 21993.55859497789,
            "unit": "iter/sec",
            "range": "stddev: 0.000006702403347173272",
            "extra": "mean: 45.46785804041482 usec\nrounds: 6976"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 114914.15874328652,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012077502707386203",
            "extra": "mean: 8.702147854851887 usec\nrounds: 19930"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 93167.677395419,
            "unit": "iter/sec",
            "range": "stddev: 0.00000146456531555246",
            "extra": "mean: 10.733336152148937 usec\nrounds: 22569"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 117925.56380473233,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011226282980507233",
            "extra": "mean: 8.479925537230038 usec\nrounds: 15412"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 142920.10503762405,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010000925084799004",
            "extra": "mean: 6.996916212290409 usec\nrounds: 28322"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 131245.49668991836,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010808047764145227",
            "extra": "mean: 7.619309044657035 usec\nrounds: 26225"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 146012.38963587928,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010333549625525861",
            "extra": "mean: 6.848733881376545 usec\nrounds: 23887"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 203662.8649939233,
            "unit": "iter/sec",
            "range": "stddev: 8.570012461537343e-7",
            "extra": "mean: 4.910075285594344 usec\nrounds: 31098"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102482.32033095279,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013413891464739778",
            "extra": "mean: 9.757780627630556 usec\nrounds: 15989"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 138915.38097224798,
            "unit": "iter/sec",
            "range": "stddev: 0.000001085617786043729",
            "extra": "mean: 7.1986269123055315 usec\nrounds: 26785"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 83895.75558162853,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016061295008933966",
            "extra": "mean: 11.919554130804915 usec\nrounds: 12020"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 45652.456939772026,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029670150998558404",
            "extra": "mean: 21.904626104116833 usec\nrounds: 8478"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 310627.37009792984,
            "unit": "iter/sec",
            "range": "stddev: 8.189357815638494e-7",
            "extra": "mean: 3.2192913318769536 usec\nrounds: 44086"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 275025.354760768,
            "unit": "iter/sec",
            "range": "stddev: 8.407585138328588e-7",
            "extra": "mean: 3.6360283977084746 usec\nrounds: 39470"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 321777.6813472555,
            "unit": "iter/sec",
            "range": "stddev: 6.496581546108012e-7",
            "extra": "mean: 3.1077357379576043 usec\nrounds: 47536"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 216515.97818150575,
            "unit": "iter/sec",
            "range": "stddev: 8.652313633591499e-7",
            "extra": "mean: 4.61859678162735 usec\nrounds: 41793"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 329489.366336906,
            "unit": "iter/sec",
            "range": "stddev: 6.725372840278659e-7",
            "extra": "mean: 3.0349993115634892 usec\nrounds: 58280"
          }
        ]
      },
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
          "id": "f106d9f30ccbe635789537fbdebdd4152b1cca6e",
          "message": "Merge pull request #83 from amsdal/bugfix/any-in-postgresql\n\nFixed ANY in postgresql",
          "timestamp": "2025-02-25T23:50:00+02:00",
          "tree_id": "2d4a1b12386764b99d7701cfc8d5403c55309598",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f106d9f30ccbe635789537fbdebdd4152b1cca6e"
        },
        "date": 1740520249999,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 48056.76071801469,
            "unit": "iter/sec",
            "range": "stddev: 0.000005133151055121098",
            "extra": "mean: 20.80872670273711 usec\nrounds: 4851"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 48864.54109662854,
            "unit": "iter/sec",
            "range": "stddev: 0.000005660914957810853",
            "extra": "mean: 20.464737364923213 usec\nrounds: 13177"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 58801.79032406406,
            "unit": "iter/sec",
            "range": "stddev: 0.000004985648212100852",
            "extra": "mean: 17.00628491902839 usec\nrounds: 5821"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 35625.32227174217,
            "unit": "iter/sec",
            "range": "stddev: 0.000008437525739186681",
            "extra": "mean: 28.069921511789243 usec\nrounds: 9519"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 150177.05352319812,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013080762308260888",
            "extra": "mean: 6.658806898522138 usec\nrounds: 25116"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 51731.63649359325,
            "unit": "iter/sec",
            "range": "stddev: 0.000005536842998055279",
            "extra": "mean: 19.33053094355223 usec\nrounds: 8973"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 82678.38784467771,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031231676779788118",
            "extra": "mean: 12.095059253920533 usec\nrounds: 8754"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57202.85248229681,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024994752987339607",
            "extra": "mean: 17.481645697816923 usec\nrounds: 10471"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 15773.874113548109,
            "unit": "iter/sec",
            "range": "stddev: 0.000013993286014725341",
            "extra": "mean: 63.395966824732334 usec\nrounds: 5700"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 33442.21538410922,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036523537225948984",
            "extra": "mean: 29.90232520526051 usec\nrounds: 9512"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 20386.43477363779,
            "unit": "iter/sec",
            "range": "stddev: 0.000008112659510192023",
            "extra": "mean: 49.0522257130082 usec\nrounds: 7070"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 14359.190757575423,
            "unit": "iter/sec",
            "range": "stddev: 0.000006020360840189401",
            "extra": "mean: 69.64180759785741 usec\nrounds: 6883"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 11218.97430401446,
            "unit": "iter/sec",
            "range": "stddev: 0.000008070265720822687",
            "extra": "mean: 89.1347081205251 usec\nrounds: 5668"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 73332.36486532172,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019105697006356425",
            "extra": "mean: 13.636543725768918 usec\nrounds: 15644"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 66173.25676498194,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019345592686065414",
            "extra": "mean: 15.111845009405483 usec\nrounds: 15571"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 28936.339013876313,
            "unit": "iter/sec",
            "range": "stddev: 0.000004000753937442712",
            "extra": "mean: 34.558621929348206 usec\nrounds: 5961"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 14882.666321113204,
            "unit": "iter/sec",
            "range": "stddev: 0.0000060920340318143025",
            "extra": "mean: 67.19226101181589 usec\nrounds: 5103"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 17463.08061564169,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052631329526718646",
            "extra": "mean: 57.26366510066383 usec\nrounds: 6165"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 20435.756581045018,
            "unit": "iter/sec",
            "range": "stddev: 0.000005871530257915846",
            "extra": "mean: 48.933837904858386 usec\nrounds: 6382"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 70371.80265815671,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018557443633647129",
            "extra": "mean: 14.210237086829709 usec\nrounds: 18699"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 51041.43381942552,
            "unit": "iter/sec",
            "range": "stddev: 0.000002225707558815057",
            "extra": "mean: 19.591926111202163 usec\nrounds: 14342"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 59220.118521454715,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019619939738040635",
            "extra": "mean: 16.88615330342023 usec\nrounds: 16109"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 45848.57264382715,
            "unit": "iter/sec",
            "range": "stddev: 0.000002395137829120925",
            "extra": "mean: 21.81092981385617 usec\nrounds: 12934"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 39936.16021512755,
            "unit": "iter/sec",
            "range": "stddev: 0.00000265039055952112",
            "extra": "mean: 25.03996364731146 usec\nrounds: 7781"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44897.54315235297,
            "unit": "iter/sec",
            "range": "stddev: 0.000002309454566352381",
            "extra": "mean: 22.272933657119104 usec\nrounds: 11343"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 24653.668264834567,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046507823170579994",
            "extra": "mean: 40.56191513805584 usec\nrounds: 5496"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 22470.396338422666,
            "unit": "iter/sec",
            "range": "stddev: 0.000005059559690633774",
            "extra": "mean: 44.50299785278269 usec\nrounds: 7621"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 114618.3797798169,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014536822883374368",
            "extra": "mean: 8.72460422072804 usec\nrounds: 15390"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 95288.02067989319,
            "unit": "iter/sec",
            "range": "stddev: 0.000001359703491218207",
            "extra": "mean: 10.494498603967862 usec\nrounds: 20907"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 120000.36032388115,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011223750652029914",
            "extra": "mean: 8.333308310916722 usec\nrounds: 15813"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 144284.65640124437,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010357439031530165",
            "extra": "mean: 6.930743884637866 usec\nrounds: 25713"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 132588.52422258843,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010340793098452726",
            "extra": "mean: 7.542130858332874 usec\nrounds: 26103"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 147360.80572986955,
            "unit": "iter/sec",
            "range": "stddev: 0.000001028203008152645",
            "extra": "mean: 6.786064958365679 usec\nrounds: 22376"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 205942.60478774668,
            "unit": "iter/sec",
            "range": "stddev: 7.78954526881349e-7",
            "extra": "mean: 4.855721821284348 usec\nrounds: 27803"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102541.83178983297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012665524969706865",
            "extra": "mean: 9.752117575289407 usec\nrounds: 15699"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 135706.08245608976,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011667266329412324",
            "extra": "mean: 7.368866464210024 usec\nrounds: 25573"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86162.03296489138,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015264154869064332",
            "extra": "mean: 11.60603998756009 usec\nrounds: 12407"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 46520.15112246723,
            "unit": "iter/sec",
            "range": "stddev: 0.000002799878195014776",
            "extra": "mean: 21.49606086548251 usec\nrounds: 8101"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 302689.8195613658,
            "unit": "iter/sec",
            "range": "stddev: 7.520737892456632e-7",
            "extra": "mean: 3.303712035803256 usec\nrounds: 39651"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 269781.770873781,
            "unit": "iter/sec",
            "range": "stddev: 7.290162755044538e-7",
            "extra": "mean: 3.7066996660343516 usec\nrounds: 34633"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 320401.5870159226,
            "unit": "iter/sec",
            "range": "stddev: 6.048197933169836e-7",
            "extra": "mean: 3.1210831672637886 usec\nrounds: 40306"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 216628.03096178622,
            "unit": "iter/sec",
            "range": "stddev: 7.863167766111583e-7",
            "extra": "mean: 4.616207771266696 usec\nrounds: 38066"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 326195.4869638402,
            "unit": "iter/sec",
            "range": "stddev: 6.148066018096715e-7",
            "extra": "mean: 3.0656463377460925 usec\nrounds: 54088"
          }
        ]
      },
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
          "id": "a0d900e94c7c508c3f464ba69829266b09145db9",
          "message": "Merge pull request #86 from amsdal/bugfix/csv-connection\n\nCSV connection fixes",
          "timestamp": "2025-03-13T16:26:52+02:00",
          "tree_id": "48cdb2e5cceb13089c0cd24aadb97e3c03f93fbb",
          "url": "https://github.com/amsdal/amsdal-glue/commit/a0d900e94c7c508c3f464ba69829266b09145db9"
        },
        "date": 1741876049042,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 50130.124162211854,
            "unit": "iter/sec",
            "range": "stddev: 0.000004626145533216815",
            "extra": "mean: 19.948085441882892 usec\nrounds: 3054"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 38909.093237323956,
            "unit": "iter/sec",
            "range": "stddev: 0.000005219396620556596",
            "extra": "mean: 25.700933041552855 usec\nrounds: 8949"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 64350.20143797896,
            "unit": "iter/sec",
            "range": "stddev: 0.000004586190540290818",
            "extra": "mean: 15.539966894490686 usec\nrounds: 11050"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53095.34808986696,
            "unit": "iter/sec",
            "range": "stddev: 0.000017482242513389473",
            "extra": "mean: 18.834041699989275 usec\nrounds: 9055"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 152477.53511246917,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021805893121326357",
            "extra": "mean: 6.558343163551198 usec\nrounds: 27137"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 71101.6357855973,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032502094136824587",
            "extra": "mean: 14.064374032342094 usec\nrounds: 12072"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 100693.53982476256,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014446111983952572",
            "extra": "mean: 9.931123702079644 usec\nrounds: 12459"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 63808.01783915015,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027260964341015927",
            "extra": "mean: 15.67201166663476 usec\nrounds: 11806"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18640.821353036445,
            "unit": "iter/sec",
            "range": "stddev: 0.000009536108414575155",
            "extra": "mean: 53.64570482497049 usec\nrounds: 4352"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37279.9410115935,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054929320572373895",
            "extra": "mean: 26.82407677868951 usec\nrounds: 11658"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22628.302205863245,
            "unit": "iter/sec",
            "range": "stddev: 0.000009174887346730232",
            "extra": "mean: 44.19244497012634 usec\nrounds: 8746"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16547.00357685359,
            "unit": "iter/sec",
            "range": "stddev: 0.000005737305982957402",
            "extra": "mean: 60.433902449796285 usec\nrounds: 5643"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13107.448089465568,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064243012534929315",
            "extra": "mean: 76.29250126908366 usec\nrounds: 6323"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 80573.62327585917,
            "unit": "iter/sec",
            "range": "stddev: 0.000001732990052788056",
            "extra": "mean: 12.41100945127302 usec\nrounds: 19161"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 69849.34940254911,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021299963981687215",
            "extra": "mean: 14.31652561625013 usec\nrounds: 16534"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33045.79432248404,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035906158810612882",
            "extra": "mean: 30.261036858164115 usec\nrounds: 8726"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16793.3639282076,
            "unit": "iter/sec",
            "range": "stddev: 0.000005710729557224945",
            "extra": "mean: 59.547330974011274 usec\nrounds: 5407"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19706.193053574047,
            "unit": "iter/sec",
            "range": "stddev: 0.000004893263469867029",
            "extra": "mean: 50.745468558100484 usec\nrounds: 7820"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23329.683453086753,
            "unit": "iter/sec",
            "range": "stddev: 0.000004633930171023888",
            "extra": "mean: 42.86384776762541 usec\nrounds: 8101"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 76136.15372000891,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018354323802136105",
            "extra": "mean: 13.134364571101203 usec\nrounds: 20173"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 56078.90604982069,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024793413483719315",
            "extra": "mean: 17.832016892619066 usec\nrounds: 16878"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 65128.08522550337,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020603059672330668",
            "extra": "mean: 15.354358976431449 usec\nrounds: 19410"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 49836.254748598796,
            "unit": "iter/sec",
            "range": "stddev: 0.000003921089946488464",
            "extra": "mean: 20.06571330539473 usec\nrounds: 364"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 43354.61746763071,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028435527424119245",
            "extra": "mean: 23.06559389542802 usec\nrounds: 7564"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 48454.40855237291,
            "unit": "iter/sec",
            "range": "stddev: 0.000002315742624980761",
            "extra": "mean: 20.637956996609095 usec\nrounds: 14999"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26698.636718645914,
            "unit": "iter/sec",
            "range": "stddev: 0.000006071143168214471",
            "extra": "mean: 37.45509594883605 usec\nrounds: 4076"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24749.3277712977,
            "unit": "iter/sec",
            "range": "stddev: 0.000004893054769048263",
            "extra": "mean: 40.40513783811617 usec\nrounds: 8817"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 122899.09582130316,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012867400786245274",
            "extra": "mean: 8.136756363561963 usec\nrounds: 22083"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 98931.6098721819,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014086619905782255",
            "extra": "mean: 10.10799279716548 usec\nrounds: 18568"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 133095.692271872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011322472433932735",
            "extra": "mean: 7.513391176908411 usec\nrounds: 16261"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 160852.09610922867,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010190530838422255",
            "extra": "mean: 6.216891319345551 usec\nrounds: 34584"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 147033.6078417638,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010284286957221792",
            "extra": "mean: 6.801166173356712 usec\nrounds: 22114"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 167171.35017714882,
            "unit": "iter/sec",
            "range": "stddev: 9.770513424999688e-7",
            "extra": "mean: 5.981886243906721 usec\nrounds: 38023"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 231253.36736063368,
            "unit": "iter/sec",
            "range": "stddev: 8.103509285174714e-7",
            "extra": "mean: 4.324261356335303 usec\nrounds: 32657"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 112983.93828970788,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012941741097610212",
            "extra": "mean: 8.850815568455836 usec\nrounds: 14102"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 154696.94788139182,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010356525087081498",
            "extra": "mean: 6.46425164617154 usec\nrounds: 34096"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 93119.87349453276,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014341014162700187",
            "extra": "mean: 10.738846204067404 usec\nrounds: 11840"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52789.55425487382,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025104908834070425",
            "extra": "mean: 18.94314157630294 usec\nrounds: 9680"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 366927.3304215312,
            "unit": "iter/sec",
            "range": "stddev: 6.934476579300816e-7",
            "extra": "mean: 2.72533528328671 usec\nrounds: 44473"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 311309.8054567773,
            "unit": "iter/sec",
            "range": "stddev: 7.152292330431836e-7",
            "extra": "mean: 3.2122341875249463 usec\nrounds: 44421"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 356143.3615347881,
            "unit": "iter/sec",
            "range": "stddev: 6.35311283895262e-7",
            "extra": "mean: 2.8078580369729003 usec\nrounds: 53367"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 225961.031828557,
            "unit": "iter/sec",
            "range": "stddev: 8.171014116312076e-7",
            "extra": "mean: 4.425541837491378 usec\nrounds: 38758"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 355172.39083994756,
            "unit": "iter/sec",
            "range": "stddev: 6.21260933717887e-7",
            "extra": "mean: 2.8155341625375185 usec\nrounds: 56076"
          }
        ]
      },
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
          "id": "2d16ae7e3e064f6444b772be59705018615725e6",
          "message": "Merge pull request #88 from amsdal/feature/remove-exception-logs\n\nRemove `exception`  logs from connections",
          "timestamp": "2025-03-14T22:39:52+02:00",
          "tree_id": "3bcb6c6905dd42097d135c4dde0bb9414dde7e2f",
          "url": "https://github.com/amsdal/amsdal-glue/commit/2d16ae7e3e064f6444b772be59705018615725e6"
        },
        "date": 1741984825960,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 74957.93895918506,
            "unit": "iter/sec",
            "range": "stddev: 0.000002192437912413895",
            "extra": "mean: 13.340815047549594 usec\nrounds: 3925"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 44687.351522546596,
            "unit": "iter/sec",
            "range": "stddev: 0.000022284716745786402",
            "extra": "mean: 22.377696729139544 usec\nrounds: 14310"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 56972.67966262636,
            "unit": "iter/sec",
            "range": "stddev: 0.000009172641982696988",
            "extra": "mean: 17.552272526440287 usec\nrounds: 11121"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 51541.01114034725,
            "unit": "iter/sec",
            "range": "stddev: 0.000003428073242257725",
            "extra": "mean: 19.402025258623254 usec\nrounds: 10303"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 107072.59922561205,
            "unit": "iter/sec",
            "range": "stddev: 0.00000269744162583749",
            "extra": "mean: 9.339457594495356 usec\nrounds: 19202"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 64677.01596409758,
            "unit": "iter/sec",
            "range": "stddev: 0.000004183743413782433",
            "extra": "mean: 15.461443065881442 usec\nrounds: 8330"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 89293.12218731154,
            "unit": "iter/sec",
            "range": "stddev: 0.000003014177953697791",
            "extra": "mean: 11.199070829915488 usec\nrounds: 11797"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 57074.629073419914,
            "unit": "iter/sec",
            "range": "stddev: 0.000004304500776909073",
            "extra": "mean: 17.52091982435165 usec\nrounds: 8149"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18473.302282525423,
            "unit": "iter/sec",
            "range": "stddev: 0.000006493980738854786",
            "extra": "mean: 54.13217326855182 usec\nrounds: 3343"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37067.77576835673,
            "unit": "iter/sec",
            "range": "stddev: 0.000003904216867846539",
            "extra": "mean: 26.97761004731392 usec\nrounds: 7385"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23359.92054529335,
            "unit": "iter/sec",
            "range": "stddev: 0.000004588042643030744",
            "extra": "mean: 42.80836478279392 usec\nrounds: 8490"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16354.844394891703,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057453850155001065",
            "extra": "mean: 61.14396296624758 usec\nrounds: 7361"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12928.701194227006,
            "unit": "iter/sec",
            "range": "stddev: 0.00000675531979783555",
            "extra": "mean: 77.34728995411585 usec\nrounds: 5793"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 78681.84388198219,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018008609193529878",
            "extra": "mean: 12.709412370914148 usec\nrounds: 16596"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68824.78018109521,
            "unit": "iter/sec",
            "range": "stddev: 0.00000203991584030344",
            "extra": "mean: 14.529650474273218 usec\nrounds: 15460"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32972.63699670624,
            "unit": "iter/sec",
            "range": "stddev: 0.000004383099689087572",
            "extra": "mean: 30.328177879733847 usec\nrounds: 8385"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16776.754588742497,
            "unit": "iter/sec",
            "range": "stddev: 0.000005533505764259409",
            "extra": "mean: 59.60628408256136 usec\nrounds: 5813"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19705.764837801635,
            "unit": "iter/sec",
            "range": "stddev: 0.000005016367866058848",
            "extra": "mean: 50.74657128160266 usec\nrounds: 7458"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23172.916837486297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045872860345073635",
            "extra": "mean: 43.1538250887054 usec\nrounds: 8136"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77165.32918631042,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017297931525683257",
            "extra": "mean: 12.959187896232104 usec\nrounds: 18758"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 54334.54901406645,
            "unit": "iter/sec",
            "range": "stddev: 0.000044262270064248685",
            "extra": "mean: 18.404496184207108 usec\nrounds: 12160"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64077.36288613192,
            "unit": "iter/sec",
            "range": "stddev: 0.00001646916388860023",
            "extra": "mean: 15.606135380087983 usec\nrounds: 19657"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 50578.41305185818,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022515288569915063",
            "extra": "mean: 19.771280664237082 usec\nrounds: 15313"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 43100.50740114784,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025185487412022433",
            "extra": "mean: 23.201583004411873 usec\nrounds: 6564"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 47848.98020190309,
            "unit": "iter/sec",
            "range": "stddev: 0.000002523491831057344",
            "extra": "mean: 20.899086997892322 usec\nrounds: 13298"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26869.34520737067,
            "unit": "iter/sec",
            "range": "stddev: 0.000004299097770541579",
            "extra": "mean: 37.217133215649966 usec\nrounds: 6616"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23994.26804017956,
            "unit": "iter/sec",
            "range": "stddev: 0.000006002752474893095",
            "extra": "mean: 41.676620363057204 usec\nrounds: 5371"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 117845.47739147923,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012785793209735787",
            "extra": "mean: 8.48568839581369 usec\nrounds: 19727"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 96438.77407379795,
            "unit": "iter/sec",
            "range": "stddev: 0.000001510391493622113",
            "extra": "mean: 10.369273247239423 usec\nrounds: 21873"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 131291.3502956504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013548637842985497",
            "extra": "mean: 7.616647995074581 usec\nrounds: 17186"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 158172.81217935783,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010295003829227816",
            "extra": "mean: 6.3221990316898715 usec\nrounds: 32311"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 144369.74463055056,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010489612613498888",
            "extra": "mean: 6.9266590625276105 usec\nrounds: 31312"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 151592.91457312528,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010935293268576855",
            "extra": "mean: 6.5966143788179545 usec\nrounds: 26187"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 215802.71782186095,
            "unit": "iter/sec",
            "range": "stddev: 8.535311576731198e-7",
            "extra": "mean: 4.633861936926446 usec\nrounds: 33194"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 110441.81445284872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014986270321392183",
            "extra": "mean: 9.054541569732478 usec\nrounds: 16468"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 142458.89659047208,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011743446353470111",
            "extra": "mean: 7.019568618973018 usec\nrounds: 28917"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 91675.78899617838,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014530486088751348",
            "extra": "mean: 10.908005384515276 usec\nrounds: 13281"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52063.720499462506,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024147498163760443",
            "extra": "mean: 19.20723279870719 usec\nrounds: 9979"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 358720.0956607082,
            "unit": "iter/sec",
            "range": "stddev: 6.140905386421079e-7",
            "extra": "mean: 2.787688819490726 usec\nrounds: 43762"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 287836.6180468071,
            "unit": "iter/sec",
            "range": "stddev: 7.746009086282656e-7",
            "extra": "mean: 3.4741931265930277 usec\nrounds: 47461"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 355043.8203410282,
            "unit": "iter/sec",
            "range": "stddev: 7.120933995942649e-7",
            "extra": "mean: 2.816553739872097 usec\nrounds: 42902"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 226881.39512110013,
            "unit": "iter/sec",
            "range": "stddev: 8.054254142359666e-7",
            "extra": "mean: 4.4075892581066 usec\nrounds: 40605"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 361931.44820317824,
            "unit": "iter/sec",
            "range": "stddev: 6.075581239730006e-7",
            "extra": "mean: 2.7629541587627604 usec\nrounds: 58547"
          }
        ]
      },
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
          "id": "98a5b79e9f45e65007123b0b31dcf5f4d44aacdf",
          "message": "Merge pull request #87 from amsdal/feature/sqlite-connection-support-inline-unique\n\nsqlite connection - support inline unique definition",
          "timestamp": "2025-03-17T13:36:09+02:00",
          "tree_id": "51cbcaf44c2bd74b2b59d94a8d5d8bd8153a7083",
          "url": "https://github.com/amsdal/amsdal-glue/commit/98a5b79e9f45e65007123b0b31dcf5f4d44aacdf"
        },
        "date": 1742211406606,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 70157.81266279309,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034518090805947544",
            "extra": "mean: 14.253580065365004 usec\nrounds: 4144"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 57939.80536521404,
            "unit": "iter/sec",
            "range": "stddev: 0.000002964967814031587",
            "extra": "mean: 17.259291668252324 usec\nrounds: 10293"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 58693.26054804307,
            "unit": "iter/sec",
            "range": "stddev: 0.00000417105721045072",
            "extra": "mean: 17.037731260158143 usec\nrounds: 10767"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 52897.55653565839,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023079476942820763",
            "extra": "mean: 18.90446488442046 usec\nrounds: 8900"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 167324.93808727257,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010023389791931252",
            "extra": "mean: 5.976395458030438 usec\nrounds: 28281"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 72676.0759953837,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020171805568368035",
            "extra": "mean: 13.75968620077285 usec\nrounds: 12346"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 95273.93323159778,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018909260939486196",
            "extra": "mean: 10.496050347466376 usec\nrounds: 12022"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 61904.69052570096,
            "unit": "iter/sec",
            "range": "stddev: 0.000003300856411332942",
            "extra": "mean: 16.153864780001285 usec\nrounds: 11990"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 14425.107978623371,
            "unit": "iter/sec",
            "range": "stddev: 0.000021823561039646118",
            "extra": "mean: 69.3235711983511 usec\nrounds: 5128"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 30741.21432476356,
            "unit": "iter/sec",
            "range": "stddev: 0.000009984526155009188",
            "extra": "mean: 32.5296193388968 usec\nrounds: 11841"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22860.994650476325,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051268181095290535",
            "extra": "mean: 43.74262866900957 usec\nrounds: 7520"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15996.619267775735,
            "unit": "iter/sec",
            "range": "stddev: 0.0000072035322639047595",
            "extra": "mean: 62.513208776209495 usec\nrounds: 7348"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13000.6220919872,
            "unit": "iter/sec",
            "range": "stddev: 0.000006721385927183678",
            "extra": "mean: 76.91939608154135 usec\nrounds: 6318"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 79336.92793139935,
            "unit": "iter/sec",
            "range": "stddev: 0.000001936625212675218",
            "extra": "mean: 12.604470907477978 usec\nrounds: 19154"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 71249.7483857227,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019596058599057506",
            "extra": "mean: 14.035137283381394 usec\nrounds: 19753"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33594.63203374766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035414084361611423",
            "extra": "mean: 29.766660310356873 usec\nrounds: 9292"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16539.82247116612,
            "unit": "iter/sec",
            "range": "stddev: 0.000006298526738967182",
            "extra": "mean: 60.46014107728788 usec\nrounds: 5964"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19226.485044310582,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056693399215155715",
            "extra": "mean: 52.01158702151414 usec\nrounds: 7783"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23352.822732782064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046369670797426865",
            "extra": "mean: 42.82137587574058 usec\nrounds: 7414"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77044.10907691356,
            "unit": "iter/sec",
            "range": "stddev: 0.000017405248366603092",
            "extra": "mean: 12.979577698817886 usec\nrounds: 20793"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 56483.88566054525,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023573936134370937",
            "extra": "mean: 17.704164440983444 usec\nrounds: 13522"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64865.98306249795,
            "unit": "iter/sec",
            "range": "stddev: 0.000017853883595690525",
            "extra": "mean: 15.416400905178707 usec\nrounds: 17579"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51780.43078971102,
            "unit": "iter/sec",
            "range": "stddev: 0.00000257383192014123",
            "extra": "mean: 19.312315188360774 usec\nrounds: 16716"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 43026.8691925743,
            "unit": "iter/sec",
            "range": "stddev: 0.000004491324418433119",
            "extra": "mean: 23.241291285320454 usec\nrounds: 8164"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46028.2708345405,
            "unit": "iter/sec",
            "range": "stddev: 0.000003033008463761241",
            "extra": "mean: 21.725778133068186 usec\nrounds: 10668"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26891.450922261127,
            "unit": "iter/sec",
            "range": "stddev: 0.000004785436706196188",
            "extra": "mean: 37.18653942811935 usec\nrounds: 4675"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24592.90866227127,
            "unit": "iter/sec",
            "range": "stddev: 0.000005402874364079128",
            "extra": "mean: 40.66212800335124 usec\nrounds: 6024"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 123393.49472100996,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013426300845838549",
            "extra": "mean: 8.104154941562994 usec\nrounds: 22950"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99449.32431067895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013768282833634683",
            "extra": "mean: 10.055372491782927 usec\nrounds: 24508"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 131598.4581502435,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012056068253051024",
            "extra": "mean: 7.598873224322421 usec\nrounds: 18031"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 160408.97505125773,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010247222396869223",
            "extra": "mean: 6.234065143053598 usec\nrounds: 28373"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 148386.64706811053,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010472523583917914",
            "extra": "mean: 6.739150858641565 usec\nrounds: 23970"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 166250.18478209226,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011409966757048757",
            "extra": "mean: 6.01503090845115 usec\nrounds: 38949"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 237825.2442184018,
            "unit": "iter/sec",
            "range": "stddev: 8.277037257227719e-7",
            "extra": "mean: 4.204768098888909 usec\nrounds: 39810"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 112206.74309992544,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012921988361132895",
            "extra": "mean: 8.91212036258331 usec\nrounds: 18554"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 152387.37614688138,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010944187685166553",
            "extra": "mean: 6.562223363148741 usec\nrounds: 34275"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 95886.22534369746,
            "unit": "iter/sec",
            "range": "stddev: 0.000001405322410483089",
            "extra": "mean: 10.42902665545098 usec\nrounds: 14908"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52285.31478441333,
            "unit": "iter/sec",
            "range": "stddev: 0.000002762661620387301",
            "extra": "mean: 19.12582919550688 usec\nrounds: 9905"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 354793.6851664137,
            "unit": "iter/sec",
            "range": "stddev: 6.474729975831998e-7",
            "extra": "mean: 2.818539454925632 usec\nrounds: 49998"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 315081.1860881677,
            "unit": "iter/sec",
            "range": "stddev: 7.920762672502887e-7",
            "extra": "mean: 3.1737851834802178 usec\nrounds: 46362"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 376904.2277412105,
            "unit": "iter/sec",
            "range": "stddev: 6.307076925024402e-7",
            "extra": "mean: 2.653193905499566 usec\nrounds: 55727"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 234393.68612992318,
            "unit": "iter/sec",
            "range": "stddev: 9.461202412540186e-7",
            "extra": "mean: 4.266326523171385 usec\nrounds: 41002"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 359172.4010937797,
            "unit": "iter/sec",
            "range": "stddev: 7.766583323271476e-7",
            "extra": "mean: 2.7841782858446873 usec\nrounds: 60067"
          }
        ]
      },
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
          "id": "a987708feb40ae54662e1cc4ae1240300ffedacd",
          "message": "Merge pull request #89 from amsdal/feature/csv-optional-dependency\n\ncsv as optional dependency",
          "timestamp": "2025-03-18T14:49:49+02:00",
          "tree_id": "e59cb2a154238e97bbd4a37f01ebd62fbca7c27b",
          "url": "https://github.com/amsdal/amsdal-glue/commit/a987708feb40ae54662e1cc4ae1240300ffedacd"
        },
        "date": 1742302212822,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 44932.50073434125,
            "unit": "iter/sec",
            "range": "stddev: 0.000010965347245459045",
            "extra": "mean: 22.255605266940208 usec\nrounds: 62"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 49818.23210583783,
            "unit": "iter/sec",
            "range": "stddev: 0.000005633173653747648",
            "extra": "mean: 20.072972438594775 usec\nrounds: 10682"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 67460.26068740388,
            "unit": "iter/sec",
            "range": "stddev: 0.0000042087046224392485",
            "extra": "mean: 14.823541886886293 usec\nrounds: 14340"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 49395.62960373665,
            "unit": "iter/sec",
            "range": "stddev: 0.00000497240412873154",
            "extra": "mean: 20.24470601999074 usec\nrounds: 7143"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 168322.56649453827,
            "unit": "iter/sec",
            "range": "stddev: 0.000001308261122209829",
            "extra": "mean: 5.940974052534115 usec\nrounds: 26979"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 70024.41593393438,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033279740634460363",
            "extra": "mean: 14.280733179459368 usec\nrounds: 11175"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 58974.45544744884,
            "unit": "iter/sec",
            "range": "stddev: 0.00002109902566182525",
            "extra": "mean: 16.956494000882866 usec\nrounds: 1124"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 39027.09692172258,
            "unit": "iter/sec",
            "range": "stddev: 0.000005386859866170455",
            "extra": "mean: 25.62322280864805 usec\nrounds: 854"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17279.348523782053,
            "unit": "iter/sec",
            "range": "stddev: 0.00001669001422949833",
            "extra": "mean: 57.87255223330161 usec\nrounds: 4672"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37439.31769341584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035564901236771804",
            "extra": "mean: 26.709888470426428 usec\nrounds: 11143"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23143.777379566945,
            "unit": "iter/sec",
            "range": "stddev: 0.000004830560807258007",
            "extra": "mean: 43.20815844361149 usec\nrounds: 7698"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16159.817836900213,
            "unit": "iter/sec",
            "range": "stddev: 0.000006406878906629566",
            "extra": "mean: 61.88188568045274 usec\nrounds: 6475"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12742.190659119673,
            "unit": "iter/sec",
            "range": "stddev: 0.000007338871848052316",
            "extra": "mean: 78.47944099661491 usec\nrounds: 6710"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 77018.54404210659,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019373430372807247",
            "extra": "mean: 12.983886055458187 usec\nrounds: 13558"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 67719.44904280048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019865735492344425",
            "extra": "mean: 14.76680649554567 usec\nrounds: 16274"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32422.762538880823,
            "unit": "iter/sec",
            "range": "stddev: 0.000003947904229354789",
            "extra": "mean: 30.842529189202097 usec\nrounds: 7750"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16697.090447098053,
            "unit": "iter/sec",
            "range": "stddev: 0.000006400880013158779",
            "extra": "mean: 59.89067395713842 usec\nrounds: 3852"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19295.700676894267,
            "unit": "iter/sec",
            "range": "stddev: 0.000005238615616079911",
            "extra": "mean: 51.825016191169205 usec\nrounds: 7262"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23184.241657563067,
            "unit": "iter/sec",
            "range": "stddev: 0.000004676036706083433",
            "extra": "mean: 43.13274571453512 usec\nrounds: 8343"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 76950.41796379464,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020453496625492984",
            "extra": "mean: 12.995381005864095 usec\nrounds: 21906"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 54146.37758282966,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027452630196340795",
            "extra": "mean: 18.468456148710303 usec\nrounds: 14941"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 65101.04211410677,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020735400387186553",
            "extra": "mean: 15.360737209816643 usec\nrounds: 20876"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51487.57555391441,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023457131173742453",
            "extra": "mean: 19.422161351389825 usec\nrounds: 16436"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 43554.93787224612,
            "unit": "iter/sec",
            "range": "stddev: 0.000004344894581318429",
            "extra": "mean: 22.959509273854696 usec\nrounds: 369"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 48798.16472031216,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025749789021245255",
            "extra": "mean: 20.492573967310527 usec\nrounds: 10877"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 27353.01532366814,
            "unit": "iter/sec",
            "range": "stddev: 0.000004506527157408701",
            "extra": "mean: 36.559040682243015 usec\nrounds: 5108"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24880.542208340794,
            "unit": "iter/sec",
            "range": "stddev: 0.000005425854767284284",
            "extra": "mean: 40.1920501420892 usec\nrounds: 6134"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 125163.35929637575,
            "unit": "iter/sec",
            "range": "stddev: 0.000001554547082500703",
            "extra": "mean: 7.989558650563929 usec\nrounds: 23670"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99136.3363392403,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015515257098176312",
            "extra": "mean: 10.087118779314608 usec\nrounds: 24662"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 128924.63143411136,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019458901006493752",
            "extra": "mean: 7.7564697209242235 usec\nrounds: 888"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 160544.67357330688,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010779034057276918",
            "extra": "mean: 6.228795871844272 usec\nrounds: 40964"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 145084.31833794992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011113482053004122",
            "extra": "mean: 6.892543670161964 usec\nrounds: 30679"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 160328.9802338879,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010571469244925484",
            "extra": "mean: 6.237175578246679 usec\nrounds: 31802"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 201928.57446670902,
            "unit": "iter/sec",
            "range": "stddev: 9.490647860069565e-7",
            "extra": "mean: 4.952246122872844 usec\nrounds: 32334"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 108883.11125304602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016312869889151962",
            "extra": "mean: 9.18416078023326 usec\nrounds: 16640"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 153752.68618022342,
            "unit": "iter/sec",
            "range": "stddev: 9.976098616876189e-7",
            "extra": "mean: 6.503951409524225 usec\nrounds: 27417"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 92652.38666680726,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015205142158173666",
            "extra": "mean: 10.793030120164733 usec\nrounds: 13028"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52159.353728433794,
            "unit": "iter/sec",
            "range": "stddev: 0.000002844648218884984",
            "extra": "mean: 19.172016685760177 usec\nrounds: 9233"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 358031.5588259329,
            "unit": "iter/sec",
            "range": "stddev: 6.377932168309346e-7",
            "extra": "mean: 2.7930498732548266 usec\nrounds: 27583"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 311368.4387469853,
            "unit": "iter/sec",
            "range": "stddev: 7.395498292123793e-7",
            "extra": "mean: 3.211629296868426 usec\nrounds: 40330"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 366339.02080483275,
            "unit": "iter/sec",
            "range": "stddev: 0.000020847673170120445",
            "extra": "mean: 2.7297119422414746 usec\nrounds: 49491"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 237589.7597631133,
            "unit": "iter/sec",
            "range": "stddev: 7.515670168499559e-7",
            "extra": "mean: 4.20893560815517 usec\nrounds: 39188"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 338088.93929815624,
            "unit": "iter/sec",
            "range": "stddev: 6.730630359173099e-7",
            "extra": "mean: 2.957801583441075 usec\nrounds: 52164"
          }
        ]
      },
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
          "id": "66186e02881f87cebf405b65aeee667779856327",
          "message": "Merge pull request #90 from amsdal/bugfix/foreign-key-name-resolve-for-sqlite\n\nBugfix: Resolve the actual FK name for sqlite.",
          "timestamp": "2025-04-01T11:17:15+03:00",
          "tree_id": "5fbdcd630de27a8c19f89c8a8c98bb82ed1f0ebe",
          "url": "https://github.com/amsdal/amsdal-glue/commit/66186e02881f87cebf405b65aeee667779856327"
        },
        "date": 1743495473538,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 68479.31314722133,
            "unit": "iter/sec",
            "range": "stddev: 0.00000385081652095794",
            "extra": "mean: 14.602950205562578 usec\nrounds: 3353"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 44962.24626512627,
            "unit": "iter/sec",
            "range": "stddev: 0.000006519020110406674",
            "extra": "mean: 22.24088169668744 usec\nrounds: 14294"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 71238.17479880848,
            "unit": "iter/sec",
            "range": "stddev: 0.0000042504823007016355",
            "extra": "mean: 14.037417477696604 usec\nrounds: 14314"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 41468.19046106826,
            "unit": "iter/sec",
            "range": "stddev: 0.00000717741769529584",
            "extra": "mean: 24.114869466967306 usec\nrounds: 4273"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 162714.56468982543,
            "unit": "iter/sec",
            "range": "stddev: 0.000001094878371773767",
            "extra": "mean: 6.1457313419130575 usec\nrounds: 24895"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 67477.71515748001,
            "unit": "iter/sec",
            "range": "stddev: 0.000002263086673965808",
            "extra": "mean: 14.819707479220249 usec\nrounds: 11072"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 90768.89256114422,
            "unit": "iter/sec",
            "range": "stddev: 0.000002085941312846392",
            "extra": "mean: 11.016990202082445 usec\nrounds: 11095"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 58484.25443393067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023185658621973284",
            "extra": "mean: 17.09861927246921 usec\nrounds: 10962"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 17919.803820748308,
            "unit": "iter/sec",
            "range": "stddev: 0.000006908287590013207",
            "extra": "mean: 55.804182345018624 usec\nrounds: 4372"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 35080.23384713792,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036866486703131038",
            "extra": "mean: 28.50608135503027 usec\nrounds: 7288"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 21696.90272739865,
            "unit": "iter/sec",
            "range": "stddev: 0.000004901317110451626",
            "extra": "mean: 46.08952773416867 usec\nrounds: 7619"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15291.252002666304,
            "unit": "iter/sec",
            "range": "stddev: 0.000006286060830800712",
            "extra": "mean: 65.39686873420385 usec\nrounds: 6301"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12144.422309811249,
            "unit": "iter/sec",
            "range": "stddev: 0.000007494817957475022",
            "extra": "mean: 82.34232757140856 usec\nrounds: 5606"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 72770.10287090846,
            "unit": "iter/sec",
            "range": "stddev: 0.000002054905630982756",
            "extra": "mean: 13.741907191940676 usec\nrounds: 15724"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 64064.812494419224,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021492447771696707",
            "extra": "mean: 15.609192645137474 usec\nrounds: 19343"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 30675.83183208916,
            "unit": "iter/sec",
            "range": "stddev: 0.000003887732208411453",
            "extra": "mean: 32.59895299575632 usec\nrounds: 8135"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 15835.304739351164,
            "unit": "iter/sec",
            "range": "stddev: 0.000006648317261170923",
            "extra": "mean: 63.15003193560101 usec\nrounds: 5250"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 18811.56451205859,
            "unit": "iter/sec",
            "range": "stddev: 0.000005671716271217009",
            "extra": "mean: 53.158789603011485 usec\nrounds: 7613"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 21960.784149534,
            "unit": "iter/sec",
            "range": "stddev: 0.000005038608153497157",
            "extra": "mean: 45.53571462616555 usec\nrounds: 8126"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 72702.46943404048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018571420476667258",
            "extra": "mean: 13.754690972460745 usec\nrounds: 20957"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 52849.50171856017,
            "unit": "iter/sec",
            "range": "stddev: 0.000002331771651831473",
            "extra": "mean: 18.921654272642098 usec\nrounds: 16357"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 61019.44526498139,
            "unit": "iter/sec",
            "range": "stddev: 0.000001975510954831545",
            "extra": "mean: 16.388218471299226 usec\nrounds: 19335"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 47702.83594735293,
            "unit": "iter/sec",
            "range": "stddev: 0.000002562123149365117",
            "extra": "mean: 20.963114249719798 usec\nrounds: 13215"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 39672.73250183269,
            "unit": "iter/sec",
            "range": "stddev: 0.000004455848021045974",
            "extra": "mean: 25.206229491598666 usec\nrounds: 5999"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45616.81765515301,
            "unit": "iter/sec",
            "range": "stddev: 0.000002697654271214016",
            "extra": "mean: 21.92173964347197 usec\nrounds: 13543"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25761.578098991406,
            "unit": "iter/sec",
            "range": "stddev: 0.000004443594494223972",
            "extra": "mean: 38.817497754112786 usec\nrounds: 6036"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23210.506341335,
            "unit": "iter/sec",
            "range": "stddev: 0.000004760664465140071",
            "extra": "mean: 43.08393730382027 usec\nrounds: 8574"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 116305.19518394725,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012729858595485176",
            "extra": "mean: 8.598068198229743 usec\nrounds: 20184"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 93484.47477871973,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015864204267046113",
            "extra": "mean: 10.696963344630506 usec\nrounds: 25777"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 122985.0683086162,
            "unit": "iter/sec",
            "range": "stddev: 0.000001475766768006541",
            "extra": "mean: 8.131068378891499 usec\nrounds: 16606"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 149996.63681319242,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012080695005771452",
            "extra": "mean: 6.666816144987382 usec\nrounds: 33442"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 128522.34412177213,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017910310534128796",
            "extra": "mean: 7.780748218010417 usec\nrounds: 28917"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 146255.28755073072,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014400323362417654",
            "extra": "mean: 6.837359638386653 usec\nrounds: 28631"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 197363.11155731376,
            "unit": "iter/sec",
            "range": "stddev: 9.506424730051194e-7",
            "extra": "mean: 5.066802970977697 usec\nrounds: 32072"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 104649.22989379824,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013673631758492881",
            "extra": "mean: 9.555732049006338 usec\nrounds: 17011"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 135424.34915999282,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012044637754219031",
            "extra": "mean: 7.384196462473535 usec\nrounds: 29876"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 84778.59678529005,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015885344180931845",
            "extra": "mean: 11.795429954244186 usec\nrounds: 12833"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 48519.46782538994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032006085183313924",
            "extra": "mean: 20.61028376483359 usec\nrounds: 9395"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 344211.91767278884,
            "unit": "iter/sec",
            "range": "stddev: 7.095851042483135e-7",
            "extra": "mean: 2.905187033502453 usec\nrounds: 36438"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 272087.2720028879,
            "unit": "iter/sec",
            "range": "stddev: 7.808026990432874e-7",
            "extra": "mean: 3.6752913601536865 usec\nrounds: 41121"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 322843.2876378994,
            "unit": "iter/sec",
            "range": "stddev: 0.00002289333678544101",
            "extra": "mean: 3.0974780591430435 usec\nrounds: 47294"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 214110.38019332092,
            "unit": "iter/sec",
            "range": "stddev: 8.367405959285037e-7",
            "extra": "mean: 4.6704881804286975 usec\nrounds: 42738"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 335946.13041911495,
            "unit": "iter/sec",
            "range": "stddev: 7.310560117546275e-7",
            "extra": "mean: 2.9766677138160045 usec\nrounds: 58394"
          }
        ]
      },
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
          "id": "7a25dcc1facc74e1262bc94a27afe4ce373c8051",
          "message": "Merge pull request #91 from amsdal/feature/improvements\n\nSQL-parser fixes and improvements",
          "timestamp": "2025-04-11T21:01:35+03:00",
          "tree_id": "548eca743b861bbce9b6e4919c94b3ea13f790f2",
          "url": "https://github.com/amsdal/amsdal-glue/commit/7a25dcc1facc74e1262bc94a27afe4ce373c8051"
        },
        "date": 1744394540081,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 51099.968351120784,
            "unit": "iter/sec",
            "range": "stddev: 0.000004433461252869021",
            "extra": "mean: 19.56948374466198 usec\nrounds: 3608"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 59083.38106097768,
            "unit": "iter/sec",
            "range": "stddev: 0.000004058006952658697",
            "extra": "mean: 16.925233154276302 usec\nrounds: 10199"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 71744.88342955397,
            "unit": "iter/sec",
            "range": "stddev: 0.0000041571732461130445",
            "extra": "mean: 13.938276183581735 usec\nrounds: 17785"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 40689.86956297696,
            "unit": "iter/sec",
            "range": "stddev: 0.000007157422860429816",
            "extra": "mean: 24.576141696700933 usec\nrounds: 10278"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 176508.25432912412,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010916884453066939",
            "extra": "mean: 5.665457424644636 usec\nrounds: 29708"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 75436.41454211697,
            "unit": "iter/sec",
            "range": "stddev: 0.000001976327758774868",
            "extra": "mean: 13.256197369265065 usec\nrounds: 12107"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 79204.26093653978,
            "unit": "iter/sec",
            "range": "stddev: 0.000003877979598637802",
            "extra": "mean: 12.62558337361701 usec\nrounds: 11418"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 63994.27808685888,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023585888993409878",
            "extra": "mean: 15.626397076355929 usec\nrounds: 8901"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 19638.55805680549,
            "unit": "iter/sec",
            "range": "stddev: 0.000005241871652819929",
            "extra": "mean: 50.92023544230952 usec\nrounds: 6510"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 38870.18785459373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034719816829773505",
            "extra": "mean: 25.726657245414334 usec\nrounds: 11333"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23816.387014046453,
            "unit": "iter/sec",
            "range": "stddev: 0.000004835790883030391",
            "extra": "mean: 41.987896796026156 usec\nrounds: 8254"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16969.360785900964,
            "unit": "iter/sec",
            "range": "stddev: 0.000005590274172353641",
            "extra": "mean: 58.9297388756595 usec\nrounds: 6895"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13515.743175123102,
            "unit": "iter/sec",
            "range": "stddev: 0.000006570705824829419",
            "extra": "mean: 73.98779238722047 usec\nrounds: 6709"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 78322.86149947095,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019283928199156616",
            "extra": "mean: 12.7676642662852 usec\nrounds: 18085"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 70671.73284772468,
            "unit": "iter/sec",
            "range": "stddev: 0.000001921076497362818",
            "extra": "mean: 14.149928970253002 usec\nrounds: 19207"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33805.25993387319,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036807442096089755",
            "extra": "mean: 29.58119541030331 usec\nrounds: 8791"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16903.40464892998,
            "unit": "iter/sec",
            "range": "stddev: 0.000005845426902092062",
            "extra": "mean: 59.15967941188121 usec\nrounds: 6205"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 20311.043830080365,
            "unit": "iter/sec",
            "range": "stddev: 0.000005097810069658952",
            "extra": "mean: 49.23429875716256 usec\nrounds: 6559"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23639.61895898502,
            "unit": "iter/sec",
            "range": "stddev: 0.00000447507087131605",
            "extra": "mean: 42.301866275214095 usec\nrounds: 8857"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77734.8618603345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018939670529819932",
            "extra": "mean: 12.864241037652974 usec\nrounds: 20805"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 56557.12156975637,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022279787427644933",
            "extra": "mean: 17.68123928949639 usec\nrounds: 16267"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 65717.89279915008,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019108620180987148",
            "extra": "mean: 15.21655606116654 usec\nrounds: 17706"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51288.41612523023,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023085124069542867",
            "extra": "mean: 19.497580068729626 usec\nrounds: 17054"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 25330.408985803213,
            "unit": "iter/sec",
            "range": "stddev: 0.000004163640792715911",
            "extra": "mean: 39.47824137227568 usec\nrounds: 7414"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22995.110775252004,
            "unit": "iter/sec",
            "range": "stddev: 0.000004912697649602342",
            "extra": "mean: 43.48750522551205 usec\nrounds: 5861"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 63370.76592648689,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023561321641351902",
            "extra": "mean: 15.780146971239827 usec\nrounds: 9072"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 50669.30196862738,
            "unit": "iter/sec",
            "range": "stddev: 0.000002608119984952672",
            "extra": "mean: 19.735815595390765 usec\nrounds: 13186"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 47523.98527658769,
            "unit": "iter/sec",
            "range": "stddev: 0.000002497037629642593",
            "extra": "mean: 21.042006350688816 usec\nrounds: 11230"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 47230.58156197393,
            "unit": "iter/sec",
            "range": "stddev: 0.000002508383170501827",
            "extra": "mean: 21.17272256509997 usec\nrounds: 14730"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 46740.05359162639,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025771148748555687",
            "extra": "mean: 21.394926260400197 usec\nrounds: 11876"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 47093.625400840305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025060806887174893",
            "extra": "mean: 21.23429639337465 usec\nrounds: 14434"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 47666.192465910455,
            "unit": "iter/sec",
            "range": "stddev: 0.000002565470919526412",
            "extra": "mean: 20.979229686012207 usec\nrounds: 14583"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 47346.32433629366,
            "unit": "iter/sec",
            "range": "stddev: 0.000002577934940598948",
            "extra": "mean: 21.12096374994506 usec\nrounds: 15307"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 47284.34444275685,
            "unit": "iter/sec",
            "range": "stddev: 0.00000287605059640701",
            "extra": "mean: 21.148648919318642 usec\nrounds: 15376"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 47420.462820009205,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025233756168709094",
            "extra": "mean: 21.087942641885117 usec\nrounds: 15175"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 47006.27374232285,
            "unit": "iter/sec",
            "range": "stddev: 0.000002852904834581807",
            "extra": "mean: 21.273756041199118 usec\nrounds: 9808"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 31784.175086620246,
            "unit": "iter/sec",
            "range": "stddev: 0.000003995721958420832",
            "extra": "mean: 31.46219769035178 usec\nrounds: 10759"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 42657.67071647385,
            "unit": "iter/sec",
            "range": "stddev: 0.000002889597581283037",
            "extra": "mean: 23.44244266515501 usec\nrounds: 13199"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 43867.00683941175,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028717825403612692",
            "extra": "mean: 22.79617580613143 usec\nrounds: 12990"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 66886.08731315791,
            "unit": "iter/sec",
            "range": "stddev: 0.000002134351673194927",
            "extra": "mean: 14.95079231227925 usec\nrounds: 18082"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 60773.15621754439,
            "unit": "iter/sec",
            "range": "stddev: 0.000003730527721083581",
            "extra": "mean: 16.454633299287384 usec\nrounds: 286"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 66899.49994659571,
            "unit": "iter/sec",
            "range": "stddev: 0.000001933720427974627",
            "extra": "mean: 14.947794838500684 usec\nrounds: 15946"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 66624.80751009085,
            "unit": "iter/sec",
            "range": "stddev: 0.000001988460722485115",
            "extra": "mean: 15.00942422758283 usec\nrounds: 15640"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 56218.836594703644,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022963590777667764",
            "extra": "mean: 17.78763241241121 usec\nrounds: 12999"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 43395.650024881084,
            "unit": "iter/sec",
            "range": "stddev: 0.000003118791554346306",
            "extra": "mean: 23.0437843292276 usec\nrounds: 8558"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 47397.70052371778,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023176863159376044",
            "extra": "mean: 21.09806992640077 usec\nrounds: 12142"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 27460.26356183892,
            "unit": "iter/sec",
            "range": "stddev: 0.000004043974106886099",
            "extra": "mean: 36.416256448087545 usec\nrounds: 7039"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24832.033704306086,
            "unit": "iter/sec",
            "range": "stddev: 0.000006127861861468653",
            "extra": "mean: 40.27056389773632 usec\nrounds: 8414"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 125770.4703171047,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013178634003983866",
            "extra": "mean: 7.950991973542781 usec\nrounds: 18607"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 101569.6759045365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013209606893727116",
            "extra": "mean: 9.845458214712448 usec\nrounds: 29207"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 135140.38122098602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011800497510897036",
            "extra": "mean: 7.399712735490711 usec\nrounds: 17129"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 167650.97677362297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010249860820402079",
            "extra": "mean: 5.964772882595772 usec\nrounds: 35099"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 151840.1920556075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010137096187224684",
            "extra": "mean: 6.585871543377501 usec\nrounds: 33685"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 172589.05953811042,
            "unit": "iter/sec",
            "range": "stddev: 9.85390446851832e-7",
            "extra": "mean: 5.794110024564935 usec\nrounds: 35668"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 238037.75186366955,
            "unit": "iter/sec",
            "range": "stddev: 7.541759754651727e-7",
            "extra": "mean: 4.201014302020153 usec\nrounds: 38409"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 109053.89002199804,
            "unit": "iter/sec",
            "range": "stddev: 0.000001249947678190306",
            "extra": "mean: 9.169778352686757 usec\nrounds: 17278"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 158622.0138187754,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010063063516308232",
            "extra": "mean: 6.304295197906726 usec\nrounds: 36473"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 95834.11594056018,
            "unit": "iter/sec",
            "range": "stddev: 0.000001470202431504232",
            "extra": "mean: 10.434697395447738 usec\nrounds: 13379"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 53821.30419269441,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025811449706792425",
            "extra": "mean: 18.58000312329365 usec\nrounds: 10218"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 372941.45934827055,
            "unit": "iter/sec",
            "range": "stddev: 6.296795595549047e-7",
            "extra": "mean: 2.6813859787740904 usec\nrounds: 50468"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 302531.4506739548,
            "unit": "iter/sec",
            "range": "stddev: 7.047034514282068e-7",
            "extra": "mean: 3.305441459961541 usec\nrounds: 50812"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 365427.44518093235,
            "unit": "iter/sec",
            "range": "stddev: 5.884711762026259e-7",
            "extra": "mean: 2.7365213346383297 usec\nrounds: 49129"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 223165.19416159877,
            "unit": "iter/sec",
            "range": "stddev: 8.618289003945979e-7",
            "extra": "mean: 4.480985503841062 usec\nrounds: 44180"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 356169.822222318,
            "unit": "iter/sec",
            "range": "stddev: 6.515125764627953e-7",
            "extra": "mean: 2.807649434644716 usec\nrounds: 57878"
          }
        ]
      },
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
          "id": "68e9cf3a2edb630154adf94fefe9e48012e9d76e",
          "message": "Merge pull request #92 from amsdal/bugfix/support-date-and-datetime-in-polars-executor\n\npolars operator constructor: support date & datetime",
          "timestamp": "2025-04-16T19:19:36+03:00",
          "tree_id": "65af7c59eb4eab3fcced273c604b7259c137b650",
          "url": "https://github.com/amsdal/amsdal-glue/commit/68e9cf3a2edb630154adf94fefe9e48012e9d76e"
        },
        "date": 1744820419229,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75524.56880637576,
            "unit": "iter/sec",
            "range": "stddev: 0.000002197968169239961",
            "extra": "mean: 13.240724386837949 usec\nrounds: 3948"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 57801.45240454714,
            "unit": "iter/sec",
            "range": "stddev: 0.000003932032411074049",
            "extra": "mean: 17.300603330883288 usec\nrounds: 8527"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 69593.85514305251,
            "unit": "iter/sec",
            "range": "stddev: 0.000004415153079180943",
            "extra": "mean: 14.369084712212972 usec\nrounds: 15401"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 49471.011730024984,
            "unit": "iter/sec",
            "range": "stddev: 0.000004979387419663737",
            "extra": "mean: 20.213857874127108 usec\nrounds: 9823"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 120519.96506110922,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028922958796095747",
            "extra": "mean: 8.297380433963399 usec\nrounds: 18666"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 72438.88076610114,
            "unit": "iter/sec",
            "range": "stddev: 0.000002269430273542389",
            "extra": "mean: 13.804741175238657 usec\nrounds: 11484"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 88391.3603821405,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027349855419033514",
            "extra": "mean: 11.313322882199358 usec\nrounds: 9591"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 46834.46916574011,
            "unit": "iter/sec",
            "range": "stddev: 0.000006251488538005275",
            "extra": "mean: 21.351795329656692 usec\nrounds: 8319"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18920.67897416828,
            "unit": "iter/sec",
            "range": "stddev: 0.000005566623570473421",
            "extra": "mean: 52.85222593572164 usec\nrounds: 6403"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37298.90427626364,
            "unit": "iter/sec",
            "range": "stddev: 0.000003364954952100292",
            "extra": "mean: 26.810439057224055 usec\nrounds: 11155"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22942.805088813802,
            "unit": "iter/sec",
            "range": "stddev: 0.000005403609705023995",
            "extra": "mean: 43.58664932770443 usec\nrounds: 7472"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16098.260410034267,
            "unit": "iter/sec",
            "range": "stddev: 0.000007310478103130364",
            "extra": "mean: 62.11851308956875 usec\nrounds: 5392"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12935.595331391756,
            "unit": "iter/sec",
            "range": "stddev: 0.000006671135792273529",
            "extra": "mean: 77.30606704843547 usec\nrounds: 6419"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 77391.7093797102,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019919120003777062",
            "extra": "mean: 12.921280690334129 usec\nrounds: 14628"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68304.36730137041,
            "unit": "iter/sec",
            "range": "stddev: 0.00000195383704644587",
            "extra": "mean: 14.640352286521168 usec\nrounds: 18633"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32874.81585017785,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035288628944377704",
            "extra": "mean: 30.418421339829038 usec\nrounds: 8362"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16131.790968982157,
            "unit": "iter/sec",
            "range": "stddev: 0.000006088714313766912",
            "extra": "mean: 61.989397328714304 usec\nrounds: 4371"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19612.94432756438,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053121581686365135",
            "extra": "mean: 50.98673525497048 usec\nrounds: 7646"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22520.686805870482,
            "unit": "iter/sec",
            "range": "stddev: 0.00000500953776748748",
            "extra": "mean: 44.40361915336123 usec\nrounds: 8253"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 74884.07515904409,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017445515332507415",
            "extra": "mean: 13.35397409764532 usec\nrounds: 19317"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 53836.96899002763,
            "unit": "iter/sec",
            "range": "stddev: 0.000002334685586915311",
            "extra": "mean: 18.574596950010925 usec\nrounds: 17798"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 62915.36321779394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019547723372782197",
            "extra": "mean: 15.89436901982593 usec\nrounds: 17826"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 49006.95910686957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026387834026332717",
            "extra": "mean: 20.40526525670156 usec\nrounds: 18094"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 24489.522759165367,
            "unit": "iter/sec",
            "range": "stddev: 0.000004968030251762253",
            "extra": "mean: 40.83378879344406 usec\nrounds: 7038"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 21943.776846565015,
            "unit": "iter/sec",
            "range": "stddev: 0.00000647080274654265",
            "extra": "mean: 45.571006622614995 usec\nrounds: 5204"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 60757.455964910674,
            "unit": "iter/sec",
            "range": "stddev: 0.000002109486133275503",
            "extra": "mean: 16.458885318989182 usec\nrounds: 15581"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 47712.888542586,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027163428468142442",
            "extra": "mean: 20.958697545788976 usec\nrounds: 11941"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45226.16531112683,
            "unit": "iter/sec",
            "range": "stddev: 0.000002919821094419479",
            "extra": "mean: 22.11109416685331 usec\nrounds: 10940"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 45333.097858186484,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026395134243419107",
            "extra": "mean: 22.05893811025789 usec\nrounds: 12787"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 45315.559326371746,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026788774278133704",
            "extra": "mean: 22.067475605846536 usec\nrounds: 15808"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 45138.69755454311,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028034674552493243",
            "extra": "mean: 22.15394005978252 usec\nrounds: 13990"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 45180.41627041785,
            "unit": "iter/sec",
            "range": "stddev: 0.000002687663420509826",
            "extra": "mean: 22.13348354328369 usec\nrounds: 13926"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 44917.278761057765,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027604826362674775",
            "extra": "mean: 22.263147447546995 usec\nrounds: 13817"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 45004.53137320514,
            "unit": "iter/sec",
            "range": "stddev: 0.000002852882590334716",
            "extra": "mean: 22.21998473236811 usec\nrounds: 13922"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 45114.08319147565,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026948816122509475",
            "extra": "mean: 22.166027308052467 usec\nrounds: 14074"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 44755.66266406994,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031240282529820784",
            "extra": "mean: 22.343541363824 usec\nrounds: 11670"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 30270.70545994727,
            "unit": "iter/sec",
            "range": "stddev: 0.000004451427616607744",
            "extra": "mean: 33.03523934462484 usec\nrounds: 10055"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 40690.76817977233,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032159171916143587",
            "extra": "mean: 24.575598956057732 usec\nrounds: 12669"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 42138.05218248965,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030607937573619563",
            "extra": "mean: 23.731519332437188 usec\nrounds: 11668"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 63615.22418797792,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022207856504871077",
            "extra": "mean: 15.719507598449699 usec\nrounds: 16964"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 58956.05480713595,
            "unit": "iter/sec",
            "range": "stddev: 0.000005220238318788849",
            "extra": "mean: 16.96178625369894 usec\nrounds: 290"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 63925.88122908345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020783762988265285",
            "extra": "mean: 15.643116383744808 usec\nrounds: 16543"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 62015.279029423655,
            "unit": "iter/sec",
            "range": "stddev: 0.00000482697764523237",
            "extra": "mean: 16.125058463826985 usec\nrounds: 19013"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 52912.8309237082,
            "unit": "iter/sec",
            "range": "stddev: 0.000002490908257300516",
            "extra": "mean: 18.89900771784143 usec\nrounds: 14137"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41612.54523314648,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028356913715012546",
            "extra": "mean: 24.031214490659174 usec\nrounds: 6489"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46634.16950551805,
            "unit": "iter/sec",
            "range": "stddev: 0.000002535709825062019",
            "extra": "mean: 21.443503992961073 usec\nrounds: 14067"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26568.624239445093,
            "unit": "iter/sec",
            "range": "stddev: 0.0000042682254629913465",
            "extra": "mean: 37.63838093337744 usec\nrounds: 6112"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24087.82815333071,
            "unit": "iter/sec",
            "range": "stddev: 0.000005096644586143258",
            "extra": "mean: 41.514743198702476 usec\nrounds: 8511"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 118698.82494995442,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017928019079599749",
            "extra": "mean: 8.424683230197251 usec\nrounds: 23015"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 97493.47301748642,
            "unit": "iter/sec",
            "range": "stddev: 0.000001411674331717189",
            "extra": "mean: 10.257096901457599 usec\nrounds: 29274"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 131669.06018815612,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012066141104708334",
            "extra": "mean: 7.594798645718229 usec\nrounds: 18402"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 159126.50203492143,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010941452627417854",
            "extra": "mean: 6.284308315786034 usec\nrounds: 35536"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 145736.37618694332,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011667795941559",
            "extra": "mean: 6.861704854780045 usec\nrounds: 31160"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 162882.77676188512,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010228067037178967",
            "extra": "mean: 6.139384530887995 usec\nrounds: 34157"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 223188.99953301004,
            "unit": "iter/sec",
            "range": "stddev: 9.073026765210763e-7",
            "extra": "mean: 4.480507561270278 usec\nrounds: 33392"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103014.18885204075,
            "unit": "iter/sec",
            "range": "stddev: 0.000001489235068419584",
            "extra": "mean: 9.707400612902944 usec\nrounds: 17526"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 150930.12279701023,
            "unit": "iter/sec",
            "range": "stddev: 0.000001065444743319937",
            "extra": "mean: 6.625582630346928 usec\nrounds: 31360"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 92263.1893763635,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016464861755919074",
            "extra": "mean: 10.83855876606175 usec\nrounds: 13291"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51920.20407662942,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026998257329962676",
            "extra": "mean: 19.260324911745194 usec\nrounds: 9682"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 360452.11920117895,
            "unit": "iter/sec",
            "range": "stddev: 6.895997726151117e-7",
            "extra": "mean: 2.7742935794528387 usec\nrounds: 36222"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 291246.68967028585,
            "unit": "iter/sec",
            "range": "stddev: 7.151538147546408e-7",
            "extra": "mean: 3.4335154199763736 usec\nrounds: 44326"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 348510.4159622872,
            "unit": "iter/sec",
            "range": "stddev: 6.180137284194943e-7",
            "extra": "mean: 2.869354699884239 usec\nrounds: 49210"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 224897.28182600994,
            "unit": "iter/sec",
            "range": "stddev: 8.147889957740005e-7",
            "extra": "mean: 4.4464743721253255 usec\nrounds: 42670"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 357247.39030288806,
            "unit": "iter/sec",
            "range": "stddev: 6.619589015626061e-7",
            "extra": "mean: 2.7991806998286584 usec\nrounds: 60391"
          }
        ]
      },
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
          "id": "f68239ad61d177815b038b8e2011ee526cdadf4a",
          "message": "Merge pull request #93 from amsdal/feature/fix-for-references\n\nFixed 'references' SQL",
          "timestamp": "2025-05-06T12:47:25+03:00",
          "tree_id": "8ee472052c4b197ee392b38d536e5ba7e30cbe97",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f68239ad61d177815b038b8e2011ee526cdadf4a"
        },
        "date": 1746524877148,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 52507.68204416064,
            "unit": "iter/sec",
            "range": "stddev: 0.000004164843393920011",
            "extra": "mean: 19.044832319182706 usec\nrounds: 3322"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 48372.308169579635,
            "unit": "iter/sec",
            "range": "stddev: 0.000005815226400425423",
            "extra": "mean: 20.672984975087044 usec\nrounds: 10816"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 90416.13349959804,
            "unit": "iter/sec",
            "range": "stddev: 0.000002071107021868276",
            "extra": "mean: 11.059973052314227 usec\nrounds: 16059"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 45520.21004995766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000063794786839788985",
            "extra": "mean: 21.968264182052696 usec\nrounds: 10047"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 180881.28691664472,
            "unit": "iter/sec",
            "range": "stddev: 9.667817848754126e-7",
            "extra": "mean: 5.52848786652446 usec\nrounds: 29980"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 67885.5473853403,
            "unit": "iter/sec",
            "range": "stddev: 0.000003921815580661884",
            "extra": "mean: 14.730675946732475 usec\nrounds: 10763"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 89594.3553934041,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030992358696447737",
            "extra": "mean: 11.161417430920203 usec\nrounds: 12157"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 63530.36452826285,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027162784812594194",
            "extra": "mean: 15.74050467717887 usec\nrounds: 8858"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 20116.693059801888,
            "unit": "iter/sec",
            "range": "stddev: 0.000005465146912618852",
            "extra": "mean: 49.70995963537599 usec\nrounds: 6689"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 40320.2185470703,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030692943054350225",
            "extra": "mean: 24.80145286991905 usec\nrounds: 12199"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 24506.220987360175,
            "unit": "iter/sec",
            "range": "stddev: 0.000004580116585444043",
            "extra": "mean: 40.80596516761112 usec\nrounds: 8801"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 17190.057382444484,
            "unit": "iter/sec",
            "range": "stddev: 0.000006169851440927158",
            "extra": "mean: 58.173162413131905 usec\nrounds: 6638"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13672.311862363234,
            "unit": "iter/sec",
            "range": "stddev: 0.000007074629703808542",
            "extra": "mean: 73.14052005738493 usec\nrounds: 6438"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 82479.1874994351,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017513827336414066",
            "extra": "mean: 12.124270744141958 usec\nrounds: 18153"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 71802.82249290212,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018404010556926594",
            "extra": "mean: 13.927029123386513 usec\nrounds: 16640"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 34487.72974267539,
            "unit": "iter/sec",
            "range": "stddev: 0.000003563341083108848",
            "extra": "mean: 28.995819889025405 usec\nrounds: 9537"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 17286.149751487454,
            "unit": "iter/sec",
            "range": "stddev: 0.000005785909047441083",
            "extra": "mean: 57.849782304121895 usec\nrounds: 6032"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 20763.131235477587,
            "unit": "iter/sec",
            "range": "stddev: 0.000004929020076903824",
            "extra": "mean: 48.1622925106459 usec\nrounds: 7474"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 24050.005324923117,
            "unit": "iter/sec",
            "range": "stddev: 0.000004348868617279634",
            "extra": "mean: 41.580032373784796 usec\nrounds: 7716"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 81102.45996743551,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016710936683827283",
            "extra": "mean: 12.330082224405064 usec\nrounds: 21303"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 58315.13788398218,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022393118658648597",
            "extra": "mean: 17.14820604539249 usec\nrounds: 16530"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 67901.4096101325,
            "unit": "iter/sec",
            "range": "stddev: 0.000001807653171872224",
            "extra": "mean: 14.727234762012603 usec\nrounds: 20152"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 53426.283103432754,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022190052650907886",
            "extra": "mean: 18.71737919824986 usec\nrounds: 18637"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 26196.900014501036,
            "unit": "iter/sec",
            "range": "stddev: 0.000004266510037914809",
            "extra": "mean: 38.17245549841622 usec\nrounds: 7304"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 23287.742704145698,
            "unit": "iter/sec",
            "range": "stddev: 0.000005998840955815015",
            "extra": "mean: 42.94104468192958 usec\nrounds: 5965"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 64567.286440816424,
            "unit": "iter/sec",
            "range": "stddev: 0.000002011338031337778",
            "extra": "mean: 15.4877191705527 usec\nrounds: 16836"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 50629.53231478435,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026021853079988814",
            "extra": "mean: 19.751318139432815 usec\nrounds: 13113"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 48093.814690150495,
            "unit": "iter/sec",
            "range": "stddev: 0.000002664939302541728",
            "extra": "mean: 20.792694579180424 usec\nrounds: 11552"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 48375.948387099,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025054118773283396",
            "extra": "mean: 20.671429363991177 usec\nrounds: 16705"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 48289.41222790145,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027417395191571414",
            "extra": "mean: 20.708473221428104 usec\nrounds: 14505"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 47957.71369330043,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026940459870635508",
            "extra": "mean: 20.851702948043112 usec\nrounds: 15271"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 47774.72517866735,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027074899344011637",
            "extra": "mean: 20.931569909825996 usec\nrounds: 18353"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 47718.521296559746,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026220819967168492",
            "extra": "mean: 20.956223554900784 usec\nrounds: 16763"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 47894.96115054571,
            "unit": "iter/sec",
            "range": "stddev: 0.000002631135060222382",
            "extra": "mean: 20.87902309507576 usec\nrounds: 15698"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 48282.5429132384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025449235893556512",
            "extra": "mean: 20.711419483372197 usec\nrounds: 14342"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 47668.15709301885,
            "unit": "iter/sec",
            "range": "stddev: 0.0000039270890280862225",
            "extra": "mean: 20.97836503409638 usec\nrounds: 12235"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 32496.760496412244,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035647486133304098",
            "extra": "mean: 30.77229806061449 usec\nrounds: 12470"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 42601.31736845816,
            "unit": "iter/sec",
            "range": "stddev: 0.000002788942242241026",
            "extra": "mean: 23.473452507372365 usec\nrounds: 12616"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 44479.46661292242,
            "unit": "iter/sec",
            "range": "stddev: 0.00000300627888138203",
            "extra": "mean: 22.482283987404525 usec\nrounds: 14447"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 67562.05255901259,
            "unit": "iter/sec",
            "range": "stddev: 0.000001927599630430261",
            "extra": "mean: 14.80120810608207 usec\nrounds: 15262"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 62156.74558299185,
            "unit": "iter/sec",
            "range": "stddev: 0.000004072911628246868",
            "extra": "mean: 16.088358401338716 usec\nrounds: 261"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 68127.89198614901,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019428494331130924",
            "extra": "mean: 14.678275972538659 usec\nrounds: 20742"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 67641.57545664476,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019361178159283616",
            "extra": "mean: 14.783807048387798 usec\nrounds: 21107"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 58220.17122103848,
            "unit": "iter/sec",
            "range": "stddev: 0.000002182852227859798",
            "extra": "mean: 17.176177586345528 usec\nrounds: 14826"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 44591.262159218844,
            "unit": "iter/sec",
            "range": "stddev: 0.000002511712663242361",
            "extra": "mean: 22.425918253432055 usec\nrounds: 8031"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 49793.041578419354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022985896399688025",
            "extra": "mean: 20.083127447137247 usec\nrounds: 12567"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 28014.109539972185,
            "unit": "iter/sec",
            "range": "stddev: 0.000004106134916677665",
            "extra": "mean: 35.69629791634608 usec\nrounds: 7368"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 26057.94475442899,
            "unit": "iter/sec",
            "range": "stddev: 0.000004133805825232909",
            "extra": "mean: 38.37601197730811 usec\nrounds: 9760"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 126003.71860612488,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014890534761479469",
            "extra": "mean: 7.936273715269473 usec\nrounds: 24127"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 103162.49690105769,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012474394345127112",
            "extra": "mean: 9.693445099134154 usec\nrounds: 19066"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 134592.94046662317,
            "unit": "iter/sec",
            "range": "stddev: 0.000002370395063284461",
            "extra": "mean: 7.429810185683428 usec\nrounds: 18599"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 165997.83455456552,
            "unit": "iter/sec",
            "range": "stddev: 9.544969169562296e-7",
            "extra": "mean: 6.024174970013165 usec\nrounds: 35358"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 154843.45475760452,
            "unit": "iter/sec",
            "range": "stddev: 9.51346665201284e-7",
            "extra": "mean: 6.458135421774351 usec\nrounds: 32677"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 174299.85203700702,
            "unit": "iter/sec",
            "range": "stddev: 9.52794132174979e-7",
            "extra": "mean: 5.737239523230817 usec\nrounds: 37041"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 242453.04989672647,
            "unit": "iter/sec",
            "range": "stddev: 7.5144155366094e-7",
            "extra": "mean: 4.124509881092248 usec\nrounds: 36438"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 114249.28602862684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012877199389002657",
            "extra": "mean: 8.752789927715042 usec\nrounds: 19136"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 158931.9967822749,
            "unit": "iter/sec",
            "range": "stddev: 9.706162206979768e-7",
            "extra": "mean: 6.2919992213394655 usec\nrounds: 30325"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 98768.03244945887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013834327702613542",
            "extra": "mean: 10.124733430441834 usec\nrounds: 14099"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 54920.60883796868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025128380284968973",
            "extra": "mean: 18.208101132860392 usec\nrounds: 10071"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 376180.86600764736,
            "unit": "iter/sec",
            "range": "stddev: 5.912519437144192e-7",
            "extra": "mean: 2.658295757072533 usec\nrounds: 52175"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 313822.5489255897,
            "unit": "iter/sec",
            "range": "stddev: 6.664742223449058e-7",
            "extra": "mean: 3.1865141731326303 usec\nrounds: 50468"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 369225.33164292865,
            "unit": "iter/sec",
            "range": "stddev: 6.121204376077541e-7",
            "extra": "mean: 2.708373219005143 usec\nrounds: 51752"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 226799.99193462223,
            "unit": "iter/sec",
            "range": "stddev: 7.964107283619905e-7",
            "extra": "mean: 4.40917123263506 usec\nrounds: 46758"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 358352.72360210394,
            "unit": "iter/sec",
            "range": "stddev: 7.187646485873606e-7",
            "extra": "mean: 2.7905466713024 usec\nrounds: 60856"
          }
        ]
      },
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
          "id": "f21ee4854be528b79e030e43b8225d4910c1149f",
          "message": "Merge pull request #94 from amsdal/feature/query-schema-improvements\n\nImproved schema query",
          "timestamp": "2025-05-14T17:50:56+03:00",
          "tree_id": "4bb5cb3b41a4613c5d61d896816ab0e5702f6e42",
          "url": "https://github.com/amsdal/amsdal-glue/commit/f21ee4854be528b79e030e43b8225d4910c1149f"
        },
        "date": 1747234301723,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 72593.40741121536,
            "unit": "iter/sec",
            "range": "stddev: 0.000004285817703302447",
            "extra": "mean: 13.77535558202086 usec\nrounds: 3614"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 60416.2831006603,
            "unit": "iter/sec",
            "range": "stddev: 0.000004187030185529453",
            "extra": "mean: 16.551829220177083 usec\nrounds: 18799"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 61720.20136065152,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037357900999019927",
            "extra": "mean: 16.202150640382225 usec\nrounds: 12210"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 35289.48347336501,
            "unit": "iter/sec",
            "range": "stddev: 0.000005705665077456359",
            "extra": "mean: 28.33705403352693 usec\nrounds: 7552"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 174912.1323729507,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015601553179714042",
            "extra": "mean: 5.717156302615891 usec\nrounds: 21402"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 72171.16422467388,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036434065145516415",
            "extra": "mean: 13.855949405041189 usec\nrounds: 13546"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 97039.2508428547,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029562302636297893",
            "extra": "mean: 10.305108410403946 usec\nrounds: 5521"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 64700.208337016404,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029191147256244514",
            "extra": "mean: 15.455900772237205 usec\nrounds: 16854"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 20688.67331893432,
            "unit": "iter/sec",
            "range": "stddev: 0.000005007726588224267",
            "extra": "mean: 48.335627161012674 usec\nrounds: 6440"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 39417.40782473625,
            "unit": "iter/sec",
            "range": "stddev: 0.00000502792544173724",
            "extra": "mean: 25.36950183143331 usec\nrounds: 14080"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 25064.36689034304,
            "unit": "iter/sec",
            "range": "stddev: 0.000004978096180369102",
            "extra": "mean: 39.89727745268868 usec\nrounds: 10222"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 17702.254877344374,
            "unit": "iter/sec",
            "range": "stddev: 0.000005713172527475949",
            "extra": "mean: 56.4899786455914 usec\nrounds: 6830"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13870.408271998642,
            "unit": "iter/sec",
            "range": "stddev: 0.000007130921992674664",
            "extra": "mean: 72.09593116439002 usec\nrounds: 7095"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 83859.27243985684,
            "unit": "iter/sec",
            "range": "stddev: 0.000001949667547725184",
            "extra": "mean: 11.924739756324401 usec\nrounds: 12721"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 72873.6612285161,
            "unit": "iter/sec",
            "range": "stddev: 0.000001956075628515675",
            "extra": "mean: 13.722379020648015 usec\nrounds: 22718"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 35673.61132494423,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036555820237187726",
            "extra": "mean: 28.03192508017166 usec\nrounds: 9431"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 17427.84521472894,
            "unit": "iter/sec",
            "range": "stddev: 0.000006084701289833311",
            "extra": "mean: 57.37944006725867 usec\nrounds: 6145"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 20961.362090451395,
            "unit": "iter/sec",
            "range": "stddev: 0.000005649281210499667",
            "extra": "mean: 47.70682342515965 usec\nrounds: 7654"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 24587.987444492544,
            "unit": "iter/sec",
            "range": "stddev: 0.00000511101465531574",
            "extra": "mean: 40.67026641596849 usec\nrounds: 7174"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 82163.57631249841,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018788923243377085",
            "extra": "mean: 12.170843150700145 usec\nrounds: 23488"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 59017.07348401392,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022576865140952734",
            "extra": "mean: 16.944249197156008 usec\nrounds: 17955"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 68572.73164060051,
            "unit": "iter/sec",
            "range": "stddev: 0.000002335294457736786",
            "extra": "mean: 14.583056210173204 usec\nrounds: 20934"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 54177.99317318361,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026200538947374417",
            "extra": "mean: 18.457678873476038 usec\nrounds: 19737"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 26904.886342604514,
            "unit": "iter/sec",
            "range": "stddev: 0.0000042373289391297435",
            "extra": "mean: 37.16796968647575 usec\nrounds: 6058"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 24281.526351909273,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047214534174748275",
            "extra": "mean: 41.183572461925124 usec\nrounds: 9416"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 66583.63008351791,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020633485395043325",
            "extra": "mean: 15.018706531104852 usec\nrounds: 20877"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 52372.24118282402,
            "unit": "iter/sec",
            "range": "stddev: 0.000002492942103345602",
            "extra": "mean: 19.094084526746578 usec\nrounds: 14597"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 48321.44016469107,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032513692930267732",
            "extra": "mean: 20.694747436991943 usec\nrounds: 5952"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 48901.57520367602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027394448183477635",
            "extra": "mean: 20.449239024202807 usec\nrounds: 15206"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 49134.7264487762,
            "unit": "iter/sec",
            "range": "stddev: 0.000002576922631705477",
            "extra": "mean: 20.352204484999366 usec\nrounds: 15950"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 48947.170261349,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027026991847606872",
            "extra": "mean: 20.430190236955276 usec\nrounds: 15723"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 48846.062640948156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026735411379847706",
            "extra": "mean: 20.472479170955523 usec\nrounds: 16038"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 48670.387429924696,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027905483794988038",
            "extra": "mean: 20.54637435216215 usec\nrounds: 16288"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 49068.940567991085,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025954499555184217",
            "extra": "mean: 20.379490333898207 usec\nrounds: 14573"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 48759.53396353508,
            "unit": "iter/sec",
            "range": "stddev: 0.000002776279768586841",
            "extra": "mean: 20.508809636036556 usec\nrounds: 15720"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 48722.61534677949,
            "unit": "iter/sec",
            "range": "stddev: 0.000002933391605072589",
            "extra": "mean: 20.524349788749568 usec\nrounds: 13748"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 33250.83725769736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038080600792476095",
            "extra": "mean: 30.074430675230776 usec\nrounds: 11514"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 44084.17465355007,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028603407890962128",
            "extra": "mean: 22.68387710235765 usec\nrounds: 8834"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 45623.27783398682,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030751445596778122",
            "extra": "mean: 21.918635562284287 usec\nrounds: 14027"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 69624.09568157651,
            "unit": "iter/sec",
            "range": "stddev: 0.000002029327471018211",
            "extra": "mean: 14.362843642141751 usec\nrounds: 16347"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 61872.45580383544,
            "unit": "iter/sec",
            "range": "stddev: 0.000004474416536055003",
            "extra": "mean: 16.16228072747697 usec\nrounds: 274"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 68908.6535886881,
            "unit": "iter/sec",
            "range": "stddev: 0.00000198061071357508",
            "extra": "mean: 14.511965448765606 usec\nrounds: 22043"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 68297.41293794259,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021135712650789314",
            "extra": "mean: 14.641843035967335 usec\nrounds: 18355"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 57639.371958623364,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023410037152578433",
            "extra": "mean: 17.349252186818653 usec\nrounds: 15762"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 45680.15588082935,
            "unit": "iter/sec",
            "range": "stddev: 0.000002742427053332628",
            "extra": "mean: 21.891343860752265 usec\nrounds: 6961"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 49872.97204140138,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029650931534583814",
            "extra": "mean: 20.050940601050673 usec\nrounds: 11302"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 28871.753320258562,
            "unit": "iter/sec",
            "range": "stddev: 0.0000043189428758980794",
            "extra": "mean: 34.6359290656008 usec\nrounds: 6484"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 25813.119642748512,
            "unit": "iter/sec",
            "range": "stddev: 0.0000059758350085242486",
            "extra": "mean: 38.73999012284912 usec\nrounds: 10240"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 129975.36820380526,
            "unit": "iter/sec",
            "range": "stddev: 0.000001202519924265031",
            "extra": "mean: 7.6937654712542916 usec\nrounds: 22391"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 104913.4026232275,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013747002798649422",
            "extra": "mean: 9.531670644514993 usec\nrounds: 20899"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 139855.07891880214,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011217943923668135",
            "extra": "mean: 7.150258737336137 usec\nrounds: 18174"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 168879.48749512562,
            "unit": "iter/sec",
            "range": "stddev: 0.000002025396803503993",
            "extra": "mean: 5.92138225211551 usec\nrounds: 37507"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 156375.60213640536,
            "unit": "iter/sec",
            "range": "stddev: 0.000001016761393427093",
            "extra": "mean: 6.394859468727781 usec\nrounds: 33915"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 178218.52178655617,
            "unit": "iter/sec",
            "range": "stddev: 9.418651178049135e-7",
            "extra": "mean: 5.611089071862309 usec\nrounds: 38299"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 245923.24433911013,
            "unit": "iter/sec",
            "range": "stddev: 8.173623507741323e-7",
            "extra": "mean: 4.066309399452592 usec\nrounds: 39286"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 108554.52767697064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013680575676426138",
            "extra": "mean: 9.211960306029184 usec\nrounds: 16880"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 145772.77035613533,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012588387314371837",
            "extra": "mean: 6.85999173615837 usec\nrounds: 31466"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 100531.44476510727,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014851347708961243",
            "extra": "mean: 9.94713646398408 usec\nrounds: 14813"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 55772.73587819942,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027089077283249092",
            "extra": "mean: 17.929907583946985 usec\nrounds: 9992"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 380469.3041458419,
            "unit": "iter/sec",
            "range": "stddev: 6.312311494081325e-7",
            "extra": "mean: 2.6283329275275222 usec\nrounds: 50016"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 307056.6456034105,
            "unit": "iter/sec",
            "range": "stddev: 6.643373930105831e-7",
            "extra": "mean: 3.2567280803672434 usec\nrounds: 53957"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 374463.6521273607,
            "unit": "iter/sec",
            "range": "stddev: 6.567658134003777e-7",
            "extra": "mean: 2.670486158853904 usec\nrounds: 61881"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 231851.33094547718,
            "unit": "iter/sec",
            "range": "stddev: 8.12703969814102e-7",
            "extra": "mean: 4.313108731884584 usec\nrounds: 46394"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 385272.708243096,
            "unit": "iter/sec",
            "range": "stddev: 6.008596061773991e-7",
            "extra": "mean: 2.5955640734589194 usec\nrounds: 69597"
          }
        ]
      },
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
          "id": "0fb53df75b3461b70918e0891174a64a03107b2e",
          "message": "Merge pull request #95 from amsdal/feature/fixes-and-improvements\n\nSynced async lock implementation with sync. Fixed copy of DeleteSchem…",
          "timestamp": "2025-05-19T16:27:34+03:00",
          "tree_id": "f2d4271d5dc03bddeec17c815ef98638dbb161c9",
          "url": "https://github.com/amsdal/amsdal-glue/commit/0fb53df75b3461b70918e0891174a64a03107b2e"
        },
        "date": 1747661298108,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75455.67246657636,
            "unit": "iter/sec",
            "range": "stddev: 0.00000410245791162239",
            "extra": "mean: 13.252814100132197 usec\nrounds: 3949"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 55400.49867542546,
            "unit": "iter/sec",
            "range": "stddev: 0.000005566050057204142",
            "extra": "mean: 18.050379038259088 usec\nrounds: 17198"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 89851.63853910318,
            "unit": "iter/sec",
            "range": "stddev: 0.000002432237062814642",
            "extra": "mean: 11.12945758429105 usec\nrounds: 15504"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 50897.452302650614,
            "unit": "iter/sec",
            "range": "stddev: 0.000005442205328742226",
            "extra": "mean: 19.647348831012557 usec\nrounds: 7504"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 178563.8212669853,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014084101416011981",
            "extra": "mean: 5.600238575230861 usec\nrounds: 30397"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 75746.08588275523,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027410596201932086",
            "extra": "mean: 13.202002299470177 usec\nrounds: 11599"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 103581.44180944239,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019172939042101643",
            "extra": "mean: 9.654239046408417 usec\nrounds: 10534"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 66304.25555303358,
            "unit": "iter/sec",
            "range": "stddev: 0.000002310787165305847",
            "extra": "mean: 15.08198820210187 usec\nrounds: 12828"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18626.12381989979,
            "unit": "iter/sec",
            "range": "stddev: 0.00001436490658033327",
            "extra": "mean: 53.68803566803414 usec\nrounds: 7208"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 40229.60876384864,
            "unit": "iter/sec",
            "range": "stddev: 0.000004268299454552549",
            "extra": "mean: 24.857313573942225 usec\nrounds: 12704"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 25077.634653153746,
            "unit": "iter/sec",
            "range": "stddev: 0.00000444340330266709",
            "extra": "mean: 39.87616909771993 usec\nrounds: 8889"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 17659.649054256355,
            "unit": "iter/sec",
            "range": "stddev: 0.000005952237200126187",
            "extra": "mean: 56.62626685998488 usec\nrounds: 6491"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 14006.888157758436,
            "unit": "iter/sec",
            "range": "stddev: 0.0000070000433250597584",
            "extra": "mean: 71.39344504911311 usec\nrounds: 6833"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 83871.83344542993,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018978722613143684",
            "extra": "mean: 11.92295385614333 usec\nrounds: 11296"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 74431.86908426748,
            "unit": "iter/sec",
            "range": "stddev: 0.000001985182987529557",
            "extra": "mean: 13.435105315813814 usec\nrounds: 20651"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 35754.01841894406,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037966573759933787",
            "extra": "mean: 27.968884176391086 usec\nrounds: 9229"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 17421.102623987732,
            "unit": "iter/sec",
            "range": "stddev: 0.000007099152701004427",
            "extra": "mean: 57.401647965902264 usec\nrounds: 4533"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 21184.67303975632,
            "unit": "iter/sec",
            "range": "stddev: 0.000005267480081101542",
            "extra": "mean: 47.203938343695235 usec\nrounds: 8680"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 24699.092084042673,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047985675717320324",
            "extra": "mean: 40.48731818146746 usec\nrounds: 8916"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 81586.79839713134,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018364369140079985",
            "extra": "mean: 12.256884932932493 usec\nrounds: 21858"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 58890.364944731584,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021878624036146045",
            "extra": "mean: 16.980706452379717 usec\nrounds: 17686"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 68516.96162595433,
            "unit": "iter/sec",
            "range": "stddev: 0.000002066023311132745",
            "extra": "mean: 14.594926223657858 usec\nrounds: 21231"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 54224.79596733589,
            "unit": "iter/sec",
            "range": "stddev: 0.00000232167485322412",
            "extra": "mean: 18.441747583566443 usec\nrounds: 17366"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 27031.835677979863,
            "unit": "iter/sec",
            "range": "stddev: 0.000004295216398759037",
            "extra": "mean: 36.99341812789282 usec\nrounds: 7871"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 24540.898382372856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045214098456374216",
            "extra": "mean: 40.74830450046915 usec\nrounds: 8961"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 65956.19475595803,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030058000620774223",
            "extra": "mean: 15.161578130758778 usec\nrounds: 9087"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 53242.68163407649,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025268671901948126",
            "extra": "mean: 18.781923999860627 usec\nrounds: 10532"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 48686.473442155024,
            "unit": "iter/sec",
            "range": "stddev: 0.000002741081586349726",
            "extra": "mean: 20.539585829483254 usec\nrounds: 12564"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 48942.38479442459,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025776126622405142",
            "extra": "mean: 20.43218785108971 usec\nrounds: 13574"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 48946.41906386354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026602394259620885",
            "extra": "mean: 20.430503786093844 usec\nrounds: 15405"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 48881.50105133137,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026125695712381476",
            "extra": "mean: 20.457636907464885 usec\nrounds: 14140"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 48758.77867741182,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027132312009543637",
            "extra": "mean: 20.50912732281508 usec\nrounds: 15745"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 49017.90105444147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026565348455407136",
            "extra": "mean: 20.400710321915973 usec\nrounds: 15264"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 49116.9539191221,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025268120699622076",
            "extra": "mean: 20.35956874782258 usec\nrounds: 15896"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 48963.82355869153,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026092297010102127",
            "extra": "mean: 20.42324163678371 usec\nrounds: 14557"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 49386.07943822317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028747903546277653",
            "extra": "mean: 20.248620894292603 usec\nrounds: 12247"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 33190.86913898495,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036673631528474615",
            "extra": "mean: 30.128768120309076 usec\nrounds: 10821"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 45254.2542056686,
            "unit": "iter/sec",
            "range": "stddev: 0.000002886687267292322",
            "extra": "mean: 22.09737001642464 usec\nrounds: 13332"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 46076.31605831702,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030369973426809164",
            "extra": "mean: 21.70312398096971 usec\nrounds: 11400"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 69134.29081285714,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021356741777222357",
            "extra": "mean: 14.464601983217662 usec\nrounds: 17657"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 62982.73473819452,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037735515861494565",
            "extra": "mean: 15.877367093645294 usec\nrounds: 290"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 68899.64357017115,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022267100593086207",
            "extra": "mean: 14.513863181041648 usec\nrounds: 24069"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 68277.36361635217,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022345331016110657",
            "extra": "mean: 14.646142543214772 usec\nrounds: 14402"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 58285.82817410301,
            "unit": "iter/sec",
            "range": "stddev: 0.000002502865338139507",
            "extra": "mean: 17.156829221212135 usec\nrounds: 15680"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 44763.816755714164,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025741689570419114",
            "extra": "mean: 22.339471306864123 usec\nrounds: 6405"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 50121.6274754864,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026068274988721735",
            "extra": "mean: 19.95146706856401 usec\nrounds: 14512"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 28726.913839445322,
            "unit": "iter/sec",
            "range": "stddev: 0.00000433256491274236",
            "extra": "mean: 34.810561468210565 usec\nrounds: 7415"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 26260.388127334085,
            "unit": "iter/sec",
            "range": "stddev: 0.000004550574658413817",
            "extra": "mean: 38.08016831857536 usec\nrounds: 9503"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 127057.37382292906,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016278345199167815",
            "extra": "mean: 7.870460170171861 usec\nrounds: 23304"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 105247.81609080349,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013799478815287976",
            "extra": "mean: 9.501384799635568 usec\nrounds: 26573"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 138320.97046575104,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011979835646271655",
            "extra": "mean: 7.229561769504827 usec\nrounds: 17641"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 170176.0706005695,
            "unit": "iter/sec",
            "range": "stddev: 0.00000102777710653772",
            "extra": "mean: 5.8762668362884 usec\nrounds: 37985"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 156665.4702716433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012147369939688067",
            "extra": "mean: 6.383027467801893 usec\nrounds: 24410"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 177525.88007997992,
            "unit": "iter/sec",
            "range": "stddev: 9.9182513748964e-7",
            "extra": "mean: 5.6329815097915565 usec\nrounds: 33384"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 244727.24429255843,
            "unit": "iter/sec",
            "range": "stddev: 8.32999037272364e-7",
            "extra": "mean: 4.0861817526313216 usec\nrounds: 35897"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 108545.63819255204,
            "unit": "iter/sec",
            "range": "stddev: 0.000001357031630763861",
            "extra": "mean: 9.21271473134713 usec\nrounds: 12915"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 161152.69338607974,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010754792623369038",
            "extra": "mean: 6.2052949844546585 usec\nrounds: 36071"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 95494.49996832566,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016400328686049352",
            "extra": "mean: 10.471807280332245 usec\nrounds: 13983"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 55691.434900038825,
            "unit": "iter/sec",
            "range": "stddev: 0.000002557973311939384",
            "extra": "mean: 17.95608250703023 usec\nrounds: 10631"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 382558.26556473545,
            "unit": "iter/sec",
            "range": "stddev: 5.905553482120491e-7",
            "extra": "mean: 2.61398090176876 usec\nrounds: 49021"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 311919.2033389726,
            "unit": "iter/sec",
            "range": "stddev: 6.994659884015494e-7",
            "extra": "mean: 3.2059584318483525 usec\nrounds: 46963"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 390612.2176731808,
            "unit": "iter/sec",
            "range": "stddev: 6.248175077644503e-7",
            "extra": "mean: 2.560083772998326 usec\nrounds: 46572"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 256916.447438418,
            "unit": "iter/sec",
            "range": "stddev: 7.856041696007376e-7",
            "extra": "mean: 3.892316003784447 usec\nrounds: 47202"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 425608.6862726477,
            "unit": "iter/sec",
            "range": "stddev: 5.55075262219918e-7",
            "extra": "mean: 2.3495761065350846 usec\nrounds: 63460"
          }
        ]
      },
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
          "id": "01e71ea784de2b8c6a7710c9997472b33735f2ba",
          "message": "Merge pull request #96 from amsdal/feature/fixes-and-improvements\n\nFeature/fixes and improvements",
          "timestamp": "2025-05-22T18:29:49+03:00",
          "tree_id": "4cd34b4d1908f213c743ab86a7b924e39c1edb54",
          "url": "https://github.com/amsdal/amsdal-glue/commit/01e71ea784de2b8c6a7710c9997472b33735f2ba"
        },
        "date": 1747927835411,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 68890.3401722472,
            "unit": "iter/sec",
            "range": "stddev: 0.000004079273612924369",
            "extra": "mean: 14.515823227170749 usec\nrounds: 3294"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 48504.78413264856,
            "unit": "iter/sec",
            "range": "stddev: 0.000006077996127533183",
            "extra": "mean: 20.61652304781417 usec\nrounds: 14847"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 86920.20246335496,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020340080569363296",
            "extra": "mean: 11.504805231230266 usec\nrounds: 9824"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 46266.39947408141,
            "unit": "iter/sec",
            "range": "stddev: 0.000006241164487814995",
            "extra": "mean: 21.613957674839238 usec\nrounds: 9596"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 132690.22523589616,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025974792917661253",
            "extra": "mean: 7.536350158590838 usec\nrounds: 25433"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 71572.48415978791,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021403330243470773",
            "extra": "mean: 13.971849821049489 usec\nrounds: 10645"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 97467.96734754418,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016409066140844914",
            "extra": "mean: 10.2597810051201 usec\nrounds: 11574"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 61039.37105243454,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027769726063112255",
            "extra": "mean: 16.382868675710498 usec\nrounds: 10207"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18888.06553830138,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061440295218977344",
            "extra": "mean: 52.9434842319978 usec\nrounds: 6469"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37700.68785322783,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037351862565016434",
            "extra": "mean: 26.524714983797907 usec\nrounds: 10669"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23401.496985294594,
            "unit": "iter/sec",
            "range": "stddev: 0.00000485370877352595",
            "extra": "mean: 42.732308989822144 usec\nrounds: 9110"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16577.82673246489,
            "unit": "iter/sec",
            "range": "stddev: 0.000005873254668017683",
            "extra": "mean: 60.321537686340264 usec\nrounds: 5948"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13142.125680675428,
            "unit": "iter/sec",
            "range": "stddev: 0.000006867202039353321",
            "extra": "mean: 76.09119135654208 usec\nrounds: 6497"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 77737.12624350259,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021730542195769256",
            "extra": "mean: 12.863866318747304 usec\nrounds: 16890"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 67126.29273491555,
            "unit": "iter/sec",
            "range": "stddev: 0.000002198461962571302",
            "extra": "mean: 14.897292242088216 usec\nrounds: 16544"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33218.071686321964,
            "unit": "iter/sec",
            "range": "stddev: 0.0000041631868844068135",
            "extra": "mean: 30.10409542862673 usec\nrounds: 8050"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16471.711487196528,
            "unit": "iter/sec",
            "range": "stddev: 0.000005742273252465149",
            "extra": "mean: 60.71014543797107 usec\nrounds: 5875"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19913.332066547457,
            "unit": "iter/sec",
            "range": "stddev: 0.000005240380659636402",
            "extra": "mean: 50.21761283637241 usec\nrounds: 7476"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23118.48239120945,
            "unit": "iter/sec",
            "range": "stddev: 0.000005610300023133522",
            "extra": "mean: 43.255434464860855 usec\nrounds: 8013"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 76005.57206673153,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019183681584191966",
            "extra": "mean: 13.15693011457131 usec\nrounds: 18715"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 56022.26833163307,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021507320065119356",
            "extra": "mean: 17.850044808616722 usec\nrounds: 12412"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64035.82050643817,
            "unit": "iter/sec",
            "range": "stddev: 0.000002033467771851013",
            "extra": "mean: 15.616259651103553 usec\nrounds: 17409"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51004.38340691664,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023146503660903964",
            "extra": "mean: 19.60615800453714 usec\nrounds: 17282"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 25259.414280617395,
            "unit": "iter/sec",
            "range": "stddev: 0.000004529396348189984",
            "extra": "mean: 39.58919984804801 usec\nrounds: 7432"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22418.951195413214,
            "unit": "iter/sec",
            "range": "stddev: 0.0000057605720810829315",
            "extra": "mean: 44.60511962774575 usec\nrounds: 4528"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 61948.5554429373,
            "unit": "iter/sec",
            "range": "stddev: 0.000003391781678901363",
            "extra": "mean: 16.142426451269397 usec\nrounds: 15205"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 49769.002217333684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025577946084349114",
            "extra": "mean: 20.092827974190673 usec\nrounds: 12041"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45834.30135375815,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027821211894212694",
            "extra": "mean: 21.817721018191232 usec\nrounds: 11405"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 45688.03288651737,
            "unit": "iter/sec",
            "range": "stddev: 0.000002588598923436279",
            "extra": "mean: 21.887569606769 usec\nrounds: 13977"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 45963.795962302655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027660243219870415",
            "extra": "mean: 21.756253570095755 usec\nrounds: 14468"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 45552.78187909156,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028566221125762455",
            "extra": "mean: 21.952556106326266 usec\nrounds: 14326"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 46090.43922578148,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026210355572522592",
            "extra": "mean: 21.696473646114285 usec\nrounds: 13444"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 46113.96985493026,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028385411957968056",
            "extra": "mean: 21.685402561217256 usec\nrounds: 15253"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 45860.829308196306,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025915938954409246",
            "extra": "mean: 21.80510067272767 usec\nrounds: 15442"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46057.049090675915,
            "unit": "iter/sec",
            "range": "stddev: 0.000002681980834844265",
            "extra": "mean: 21.712203012208317 usec\nrounds: 13752"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 45556.730257070405,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031899114291288214",
            "extra": "mean: 21.950653489772783 usec\nrounds: 11571"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 30932.57520732639,
            "unit": "iter/sec",
            "range": "stddev: 0.0000044286539443248366",
            "extra": "mean: 32.32837852320649 usec\nrounds: 9635"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41353.62787579836,
            "unit": "iter/sec",
            "range": "stddev: 0.000003042766990469037",
            "extra": "mean: 24.18167525720848 usec\nrounds: 11953"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 42266.11555671546,
            "unit": "iter/sec",
            "range": "stddev: 0.000003244836648181262",
            "extra": "mean: 23.659614488540686 usec\nrounds: 11007"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 65154.004010895376,
            "unit": "iter/sec",
            "range": "stddev: 0.000002129185588639496",
            "extra": "mean: 15.348250889274203 usec\nrounds: 17316"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 59975.295542816566,
            "unit": "iter/sec",
            "range": "stddev: 0.000004044923925397366",
            "extra": "mean: 16.67353184255835 usec\nrounds: 292"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 65540.320791868,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019555117237687997",
            "extra": "mean: 15.257783116070378 usec\nrounds: 22090"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 64817.221529014074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021965098822196866",
            "extra": "mean: 15.427998553630857 usec\nrounds: 16246"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 53099.355244093866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024840260263690586",
            "extra": "mean: 18.83262038499475 usec\nrounds: 11984"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41877.902054528866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026948713173962173",
            "extra": "mean: 23.878942137500307 usec\nrounds: 6714"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45605.377361653234,
            "unit": "iter/sec",
            "range": "stddev: 0.000003086529685363109",
            "extra": "mean: 21.927238800590185 usec\nrounds: 12638"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26818.704789965544,
            "unit": "iter/sec",
            "range": "stddev: 0.0000045287437538484925",
            "extra": "mean: 37.28740846478757 usec\nrounds: 6583"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 23904.44483588608,
            "unit": "iter/sec",
            "range": "stddev: 0.000006568091304300742",
            "extra": "mean: 41.83322419179422 usec\nrounds: 7714"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 120989.34438880807,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011259314535935433",
            "extra": "mean: 8.26519066659645 usec\nrounds: 18358"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 98044.89598988705,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013145845745321366",
            "extra": "mean: 10.199409055450944 usec\nrounds: 26338"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 126828.21787389305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028441542869921083",
            "extra": "mean: 7.884680686708954 usec\nrounds: 17501"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 161288.5858967722,
            "unit": "iter/sec",
            "range": "stddev: 9.91340991292991e-7",
            "extra": "mean: 6.200066758846899 usec\nrounds: 33920"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 146151.7090921224,
            "unit": "iter/sec",
            "range": "stddev: 0.000001024977784814191",
            "extra": "mean: 6.842205309892611 usec\nrounds: 31787"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 164055.70933824903,
            "unit": "iter/sec",
            "range": "stddev: 9.68235240014374e-7",
            "extra": "mean: 6.095490391853454 usec\nrounds: 27777"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 224558.35563587365,
            "unit": "iter/sec",
            "range": "stddev: 9.00490503429852e-7",
            "extra": "mean: 4.453185441122138 usec\nrounds: 38624"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 111305.99344646321,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014398330548411279",
            "extra": "mean: 8.984242169142378 usec\nrounds: 14489"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 151432.37609957717,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010308225293588112",
            "extra": "mean: 6.603607668035476 usec\nrounds: 33043"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88768.12226793295,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018018904205407202",
            "extra": "mean: 11.26530531964677 usec\nrounds: 13432"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51886.455024822746,
            "unit": "iter/sec",
            "range": "stddev: 0.000002711959783719789",
            "extra": "mean: 19.272852607132148 usec\nrounds: 9689"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 343219.921332796,
            "unit": "iter/sec",
            "range": "stddev: 7.134158985531366e-7",
            "extra": "mean: 2.9135837923299652 usec\nrounds: 45552"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 287746.38125935866,
            "unit": "iter/sec",
            "range": "stddev: 7.344885044255216e-7",
            "extra": "mean: 3.475282627789697 usec\nrounds: 44319"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 356062.4768435304,
            "unit": "iter/sec",
            "range": "stddev: 5.971038180207668e-7",
            "extra": "mean: 2.808495882141055 usec\nrounds: 49527"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 233167.22777742072,
            "unit": "iter/sec",
            "range": "stddev: 9.226959761617264e-7",
            "extra": "mean: 4.288767377526103 usec\nrounds: 42274"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 386424.13886014506,
            "unit": "iter/sec",
            "range": "stddev: 5.743788809319037e-7",
            "extra": "mean: 2.587830053654906 usec\nrounds: 68619"
          }
        ]
      },
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
          "id": "05cde8b777e4542e5e84c89e5bdef95cc4dc662f",
          "message": "Merge pull request #97 from amsdal/bugfix/retrieve-fk-name\n\nFixed retrieving FK name for sqlite.",
          "timestamp": "2025-06-10T00:10:59+03:00",
          "tree_id": "2c53aadc9c2ed6376fed2b7f7153e8f17cb4dd9c",
          "url": "https://github.com/amsdal/amsdal-glue/commit/05cde8b777e4542e5e84c89e5bdef95cc4dc662f"
        },
        "date": 1749503498383,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 78646.71198812724,
            "unit": "iter/sec",
            "range": "stddev: 0.000002091905334217161",
            "extra": "mean: 12.715089731290522 usec\nrounds: 4505"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 55620.386144478995,
            "unit": "iter/sec",
            "range": "stddev: 0.00000478535273258253",
            "extra": "mean: 17.979019372544617 usec\nrounds: 15965"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 83093.6699539277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030734441116017247",
            "extra": "mean: 12.034611066696923 usec\nrounds: 15911"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53288.70148328772,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034156015761732197",
            "extra": "mean: 18.76570402665221 usec\nrounds: 6676"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 145213.5579360585,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024042104519280873",
            "extra": "mean: 6.886409328530656 usec\nrounds: 26990"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 73052.80117095046,
            "unit": "iter/sec",
            "range": "stddev: 0.000002191771446600487",
            "extra": "mean: 13.688729028472233 usec\nrounds: 11425"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 97405.43314473415,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019741069515314875",
            "extra": "mean: 10.266367775543957 usec\nrounds: 10365"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 63006.032372610236,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021460491094257302",
            "extra": "mean: 15.871496146370845 usec\nrounds: 11681"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 19550.25440016078,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058068015229489685",
            "extra": "mean: 51.150229533165366 usec\nrounds: 6394"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 38570.96465270279,
            "unit": "iter/sec",
            "range": "stddev: 0.000003516888944181762",
            "extra": "mean: 25.926237754334384 usec\nrounds: 10977"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23534.518818085737,
            "unit": "iter/sec",
            "range": "stddev: 0.000004903891175045861",
            "extra": "mean: 42.490777386598744 usec\nrounds: 8076"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16647.133717380464,
            "unit": "iter/sec",
            "range": "stddev: 0.000006399000053959459",
            "extra": "mean: 60.070401125927674 usec\nrounds: 627"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13132.204808943225,
            "unit": "iter/sec",
            "range": "stddev: 0.000006826842642161728",
            "extra": "mean: 76.14867530233654 usec\nrounds: 5938"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 78958.12373979455,
            "unit": "iter/sec",
            "range": "stddev: 0.000002001979356785867",
            "extra": "mean: 12.66494127058397 usec\nrounds: 18802"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 69170.63530283919,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019681329261989596",
            "extra": "mean: 14.457001813296253 usec\nrounds: 18275"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33586.513104248515,
            "unit": "iter/sec",
            "range": "stddev: 0.000003877570382284734",
            "extra": "mean: 29.77385585982444 usec\nrounds: 8531"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16606.975942298253,
            "unit": "iter/sec",
            "range": "stddev: 0.000005899795598825807",
            "extra": "mean: 60.215658978163674 usec\nrounds: 4699"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 20134.266457605543,
            "unit": "iter/sec",
            "range": "stddev: 0.000005164107102580646",
            "extra": "mean: 49.66657226403491 usec\nrounds: 7629"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23578.363969225244,
            "unit": "iter/sec",
            "range": "stddev: 0.000004475784133214934",
            "extra": "mean: 42.41176365354321 usec\nrounds: 8458"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 75922.78538786333,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017829552330535111",
            "extra": "mean: 13.171276513254156 usec\nrounds: 20310"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 56462.60271344873,
            "unit": "iter/sec",
            "range": "stddev: 0.000002165039038813716",
            "extra": "mean: 17.710837827917054 usec\nrounds: 16686"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 65353.31684035635,
            "unit": "iter/sec",
            "range": "stddev: 0.000002059258785965904",
            "extra": "mean: 15.301442196771406 usec\nrounds: 20313"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51359.41960688025,
            "unit": "iter/sec",
            "range": "stddev: 0.000002547205556826708",
            "extra": "mean: 19.470625012009233 usec\nrounds: 16875"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 25584.061653883866,
            "unit": "iter/sec",
            "range": "stddev: 0.000004297540236308847",
            "extra": "mean: 39.0868351369921 usec\nrounds: 6973"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 23061.420304584542,
            "unit": "iter/sec",
            "range": "stddev: 0.000005644185358770063",
            "extra": "mean: 43.3624636640963 usec\nrounds: 5593"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 64021.39239351324,
            "unit": "iter/sec",
            "range": "stddev: 0.000001941026029640745",
            "extra": "mean: 15.61977899283118 usec\nrounds: 15261"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 50240.47718501954,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026349161614751093",
            "extra": "mean: 19.904269545795138 usec\nrounds: 12166"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 46384.844845863234,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027624871715298707",
            "extra": "mean: 21.558765655528187 usec\nrounds: 11146"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 46554.39684305793,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027135947620988907",
            "extra": "mean: 21.480248221691166 usec\nrounds: 14047"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 46547.97960783615,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027364681024205384",
            "extra": "mean: 21.483209549048922 usec\nrounds: 14277"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 46504.13816735905,
            "unit": "iter/sec",
            "range": "stddev: 0.000002652190219109327",
            "extra": "mean: 21.503462689733137 usec\nrounds: 17405"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 46491.04640531858,
            "unit": "iter/sec",
            "range": "stddev: 0.000002593143784003284",
            "extra": "mean: 21.50951801088306 usec\nrounds: 14917"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 46457.90713287298,
            "unit": "iter/sec",
            "range": "stddev: 0.000002736931110153074",
            "extra": "mean: 21.524861142365445 usec\nrounds: 15397"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 46457.35304178434,
            "unit": "iter/sec",
            "range": "stddev: 0.000002686516489661867",
            "extra": "mean: 21.52511786671503 usec\nrounds: 14824"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46468.46585910866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025730250491269638",
            "extra": "mean: 21.51997018864314 usec\nrounds: 14867"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 46927.66377502481,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029983670751192094",
            "extra": "mean: 21.309392361701292 usec\nrounds: 11850"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 31698.94528253461,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037490245127481664",
            "extra": "mean: 31.546790944838698 usec\nrounds: 9830"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41919.587897317615,
            "unit": "iter/sec",
            "range": "stddev: 0.00000287923691384209",
            "extra": "mean: 23.855196345190905 usec\nrounds: 10179"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 43597.90849384872,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031651492362487357",
            "extra": "mean: 22.936880106097085 usec\nrounds: 11799"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 66015.40609842107,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021532323660593625",
            "extra": "mean: 15.147979223351587 usec\nrounds: 14118"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 61245.224388389186,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022822724560490375",
            "extra": "mean: 16.32780367753178 usec\nrounds: 15684"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 65064.768762439126,
            "unit": "iter/sec",
            "range": "stddev: 0.000001993817173147845",
            "extra": "mean: 15.369300760157076 usec\nrounds: 12541"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 64881.44038871505,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019741952442231167",
            "extra": "mean: 15.412728108513633 usec\nrounds: 17865"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 54921.76952001384,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024176744254083394",
            "extra": "mean: 18.207716334332485 usec\nrounds: 14570"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41870.82792071881,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031310461538043846",
            "extra": "mean: 23.882976517528405 usec\nrounds: 8198"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46285.02987756027,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024361131613842633",
            "extra": "mean: 21.605257739820885 usec\nrounds: 12072"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 27320.20057100245,
            "unit": "iter/sec",
            "range": "stddev: 0.000004183474128726367",
            "extra": "mean: 36.602952361242764 usec\nrounds: 7018"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24827.909328156195,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047261828486337596",
            "extra": "mean: 40.27725358517987 usec\nrounds: 8334"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 124394.19228459297,
            "unit": "iter/sec",
            "range": "stddev: 0.000001265330327929338",
            "extra": "mean: 8.038960514427943 usec\nrounds: 23461"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 100497.9298858921,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012882641116640422",
            "extra": "mean: 9.950453717160398 usec\nrounds: 25595"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 130910.34134465863,
            "unit": "iter/sec",
            "range": "stddev: 0.000001630585247344163",
            "extra": "mean: 7.638815923390009 usec\nrounds: 16893"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 159236.60022952716,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012747537832555875",
            "extra": "mean: 6.279963265722691 usec\nrounds: 30923"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 146817.05508843675,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011604584152395758",
            "extra": "mean: 6.8111977821489464 usec\nrounds: 29124"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 167422.01604007214,
            "unit": "iter/sec",
            "range": "stddev: 9.473608407008349e-7",
            "extra": "mean: 5.972930105922581 usec\nrounds: 30013"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 228956.19717832867,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016831146465586659",
            "extra": "mean: 4.36764766502967 usec\nrounds: 35113"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 102447.57968317276,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013327195898912652",
            "extra": "mean: 9.761089555190852 usec\nrounds: 16470"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137625.56213621816,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011651336322799587",
            "extra": "mean: 7.266092028821117 usec\nrounds: 18369"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 95829.89371416999,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016637839925719978",
            "extra": "mean: 10.435157143998104 usec\nrounds: 13992"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 53357.054273375084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027560190666073386",
            "extra": "mean: 18.741664314459637 usec\nrounds: 9053"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 367869.9196379129,
            "unit": "iter/sec",
            "range": "stddev: 6.045626536201319e-7",
            "extra": "mean: 2.718352185425436 usec\nrounds: 50985"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 323868.8122932924,
            "unit": "iter/sec",
            "range": "stddev: 6.842587716246248e-7",
            "extra": "mean: 3.087669951666757 usec\nrounds: 44613"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 375902.79127218045,
            "unit": "iter/sec",
            "range": "stddev: 5.866102675944663e-7",
            "extra": "mean: 2.6602622359245225 usec\nrounds: 56740"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 230343.0735085658,
            "unit": "iter/sec",
            "range": "stddev: 7.757639696452298e-7",
            "extra": "mean: 4.341350424686475 usec\nrounds: 41522"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 394530.4298294073,
            "unit": "iter/sec",
            "range": "stddev: 5.81666970926589e-7",
            "extra": "mean: 2.534658734517371 usec\nrounds: 59999"
          }
        ]
      },
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
          "id": "7feb5ec831a66390528e06db3926f6a6349e68e9",
          "message": "Merge pull request #98 from amsdal/bugix/postgres-json-type\n\nJsonType for postgres instead of dict",
          "timestamp": "2025-06-10T20:11:02+03:00",
          "tree_id": "906efb79808fb1c14fb95323d0989c8be1b281be",
          "url": "https://github.com/amsdal/amsdal-glue/commit/7feb5ec831a66390528e06db3926f6a6349e68e9"
        },
        "date": 1749575491255,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 75671.86203231056,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024526949419721804",
            "extra": "mean: 13.214951676133165 usec\nrounds: 4154"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 58417.85133766174,
            "unit": "iter/sec",
            "range": "stddev: 0.000003559502279853905",
            "extra": "mean: 17.11805513386461 usec\nrounds: 16732"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 87627.59590355892,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015710024749833544",
            "extra": "mean: 11.411930108188507 usec\nrounds: 15742"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53161.537904414676,
            "unit": "iter/sec",
            "range": "stddev: 0.000002402464156824851",
            "extra": "mean: 18.810592007289493 usec\nrounds: 8987"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 170598.68521790832,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010308187356179478",
            "extra": "mean: 5.861709887873313 usec\nrounds: 26047"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 70923.36408212119,
            "unit": "iter/sec",
            "range": "stddev: 0.000002696534475790102",
            "extra": "mean: 14.099725992158435 usec\nrounds: 11016"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 87448.17576039692,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032426815450965797",
            "extra": "mean: 11.43534432027426 usec\nrounds: 9212"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 54636.61960876863,
            "unit": "iter/sec",
            "range": "stddev: 0.000004917973438861247",
            "extra": "mean: 18.302742870269192 usec\nrounds: 11329"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18820.377720276425,
            "unit": "iter/sec",
            "range": "stddev: 0.000006657118984986548",
            "extra": "mean: 53.13389640010437 usec\nrounds: 6541"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37682.49752732177,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032175284354195918",
            "extra": "mean: 26.537519156604414 usec\nrounds: 11071"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 22842.25016122689,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047938150152728595",
            "extra": "mean: 43.77852413583271 usec\nrounds: 7516"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 15947.33161224812,
            "unit": "iter/sec",
            "range": "stddev: 0.00000743871731922938",
            "extra": "mean: 62.70641536242743 usec\nrounds: 619"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12936.122524475673,
            "unit": "iter/sec",
            "range": "stddev: 0.000006936386806069523",
            "extra": "mean: 77.30291655076388 usec\nrounds: 5232"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 77380.25330398882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019862042164171063",
            "extra": "mean: 12.923193674121144 usec\nrounds: 14751"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 68784.21770225513,
            "unit": "iter/sec",
            "range": "stddev: 0.000001964881788645713",
            "extra": "mean: 14.53821869907251 usec\nrounds: 16370"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32121.087979037624,
            "unit": "iter/sec",
            "range": "stddev: 0.00000437779134716326",
            "extra": "mean: 31.132195791518793 usec\nrounds: 8296"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16271.048543580268,
            "unit": "iter/sec",
            "range": "stddev: 0.000005521379759346207",
            "extra": "mean: 61.45885419256212 usec\nrounds: 5623"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19282.025197860126,
            "unit": "iter/sec",
            "range": "stddev: 0.000005780957423071202",
            "extra": "mean: 51.861772284737896 usec\nrounds: 7521"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22753.237514821947,
            "unit": "iter/sec",
            "range": "stddev: 0.000005044783956960033",
            "extra": "mean: 43.94978953428401 usec\nrounds: 5817"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 75368.75024834916,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017774364400254946",
            "extra": "mean: 13.268098471911486 usec\nrounds: 18565"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 54458.80818711574,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024751553128286423",
            "extra": "mean: 18.362502472769634 usec\nrounds: 16807"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 63259.22089610415,
            "unit": "iter/sec",
            "range": "stddev: 0.000002079042975058861",
            "extra": "mean: 15.807972115913076 usec\nrounds: 20947"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 50182.80831455232,
            "unit": "iter/sec",
            "range": "stddev: 0.000002217746447261721",
            "extra": "mean: 19.92714305129898 usec\nrounds: 17208"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 24705.42085097818,
            "unit": "iter/sec",
            "range": "stddev: 0.000004304177506021911",
            "extra": "mean: 40.476946579131294 usec\nrounds: 7225"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22182.532693997437,
            "unit": "iter/sec",
            "range": "stddev: 0.000004866622240852986",
            "extra": "mean: 45.08051509693475 usec\nrounds: 5680"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 60486.097032570266,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025093979450773317",
            "extra": "mean: 16.532724858433582 usec\nrounds: 10373"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 48792.23153315083,
            "unit": "iter/sec",
            "range": "stddev: 0.000002426288875535727",
            "extra": "mean: 20.495065886063678 usec\nrounds: 12559"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45060.42426004672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028673670522480068",
            "extra": "mean: 22.192423094574814 usec\nrounds: 10261"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 44859.71419175553,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029909019579303452",
            "extra": "mean: 22.291715808206895 usec\nrounds: 11441"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 45208.60901270305,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025539613829478645",
            "extra": "mean: 22.119680782901607 usec\nrounds: 16779"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 45302.506421817736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027087949665916592",
            "extra": "mean: 22.07383385565614 usec\nrounds: 14565"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 45490.7833879114,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025765896879998754",
            "extra": "mean: 21.982474811936026 usec\nrounds: 14612"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 45015.559654398945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029047114383483153",
            "extra": "mean: 22.21454109817514 usec\nrounds: 14419"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 45170.03558456453,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026850502153152206",
            "extra": "mean: 22.138570117525415 usec\nrounds: 14136"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 45271.4286628859,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026152406651699648",
            "extra": "mean: 22.088987017540553 usec\nrounds: 15200"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 45489.897962772855,
            "unit": "iter/sec",
            "range": "stddev: 0.000002863874303481799",
            "extra": "mean: 21.982902683544392 usec\nrounds: 11797"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 30517.789403914303,
            "unit": "iter/sec",
            "range": "stddev: 0.000003824001374129983",
            "extra": "mean: 32.76777314256376 usec\nrounds: 9743"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 40589.68761105888,
            "unit": "iter/sec",
            "range": "stddev: 0.000003008730116104301",
            "extra": "mean: 24.636799612311986 usec\nrounds: 13338"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 42684.829455492516,
            "unit": "iter/sec",
            "range": "stddev: 0.000003088928049565965",
            "extra": "mean: 23.427527127470434 usec\nrounds: 12661"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 62981.93028972529,
            "unit": "iter/sec",
            "range": "stddev: 0.000002439417469267763",
            "extra": "mean: 15.877569890282285 usec\nrounds: 15772"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 58266.760638806045,
            "unit": "iter/sec",
            "range": "stddev: 0.000002555675261868733",
            "extra": "mean: 17.162443716392108 usec\nrounds: 14634"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 64114.378356736066,
            "unit": "iter/sec",
            "range": "stddev: 0.000001929113463346212",
            "extra": "mean: 15.597125412897912 usec\nrounds: 11382"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 63560.14105612765,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019849670773523847",
            "extra": "mean: 15.733130597003182 usec\nrounds: 18580"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 52284.29079567148,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023921841722279403",
            "extra": "mean: 19.12620377520332 usec\nrounds: 10593"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41509.57041955429,
            "unit": "iter/sec",
            "range": "stddev: 0.00000295927730657521",
            "extra": "mean: 24.090829895192577 usec\nrounds: 7451"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46996.48722237331,
            "unit": "iter/sec",
            "range": "stddev: 0.000002374709380054528",
            "extra": "mean: 21.278186075233652 usec\nrounds: 10908"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 25777.37765166768,
            "unit": "iter/sec",
            "range": "stddev: 0.000006630714512340993",
            "extra": "mean: 38.793705609356444 usec\nrounds: 5582"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24192.302263993613,
            "unit": "iter/sec",
            "range": "stddev: 0.000004240976639107287",
            "extra": "mean: 41.33546237508535 usec\nrounds: 8587"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 121558.33863656284,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012584296358632942",
            "extra": "mean: 8.226502691763638 usec\nrounds: 22242"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 97888.30506638618,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013171490246164763",
            "extra": "mean: 10.21572494611912 usec\nrounds: 29724"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 126406.20906084494,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013119265094250477",
            "extra": "mean: 7.911003798228419 usec\nrounds: 16590"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 159401.0105353124,
            "unit": "iter/sec",
            "range": "stddev: 0.000001049129317636989",
            "extra": "mean: 6.27348594994301 usec\nrounds: 30965"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 145510.02013155186,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010944895179594544",
            "extra": "mean: 6.872378954356035 usec\nrounds: 28977"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 161710.52171422532,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010436992170658914",
            "extra": "mean: 6.183889516893644 usec\nrounds: 32745"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 213150.81137032283,
            "unit": "iter/sec",
            "range": "stddev: 9.622244064076817e-7",
            "extra": "mean: 4.691513926553276 usec\nrounds: 31073"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 99905.85483783999,
            "unit": "iter/sec",
            "range": "stddev: 0.000001451729634647415",
            "extra": "mean: 10.009423387879803 usec\nrounds: 17166"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 134963.3098101262,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011381636999294722",
            "extra": "mean: 7.409421133838929 usec\nrounds: 20921"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 86859.09777245375,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015593508153992986",
            "extra": "mean: 11.512898771061575 usec\nrounds: 13521"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51455.57346375177,
            "unit": "iter/sec",
            "range": "stddev: 0.000002634469506587414",
            "extra": "mean: 19.43424069900721 usec\nrounds: 9892"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 352256.3725518757,
            "unit": "iter/sec",
            "range": "stddev: 6.816170489115203e-7",
            "extra": "mean: 2.838841474337652 usec\nrounds: 45793"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 282139.5852822574,
            "unit": "iter/sec",
            "range": "stddev: 8.17829871018306e-7",
            "extra": "mean: 3.544344899350378 usec\nrounds: 48780"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 354572.6617721428,
            "unit": "iter/sec",
            "range": "stddev: 5.999883461293823e-7",
            "extra": "mean: 2.8202963956725595 usec\nrounds: 49564"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 220501.32580435806,
            "unit": "iter/sec",
            "range": "stddev: 7.839845191317712e-7",
            "extra": "mean: 4.535120123891045 usec\nrounds: 42603"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 381489.90727472387,
            "unit": "iter/sec",
            "range": "stddev: 6.399167896291721e-7",
            "extra": "mean: 2.621301326537758 usec\nrounds: 63162"
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
          "id": "bd814b8cd227ca95f016a91261c0d0200c288f72",
          "message": "Merge pull request #99 from amsdal/feature/uv-installer\n\nUse UV as installer. Updated GitHub actions.",
          "timestamp": "2025-06-16T19:00:45+03:00",
          "tree_id": "ee45ccb99363a3095b6a4c8c12cbdfb410ab8cf3",
          "url": "https://github.com/amsdal/amsdal-glue/commit/bd814b8cd227ca95f016a91261c0d0200c288f72"
        },
        "date": 1750089677496,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 77550.58092145574,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022599255481034825",
            "extra": "mean: 12.894809917836893 usec\nrounds: 3416"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 61583.662426618335,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019926849756010616",
            "extra": "mean: 16.23807290109738 usec\nrounds: 12343"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 87630.54067318972,
            "unit": "iter/sec",
            "range": "stddev: 0.000001438068286216662",
            "extra": "mean: 11.411546617399186 usec\nrounds: 15452"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53276.375218037385,
            "unit": "iter/sec",
            "range": "stddev: 0.000002631157601570155",
            "extra": "mean: 18.770045745556605 usec\nrounds: 8430"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 170871.6687694784,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010085578322534105",
            "extra": "mean: 5.852345255368764 usec\nrounds: 25225"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 71775.90638395678,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017797364832518955",
            "extra": "mean: 13.932251787258771 usec\nrounds: 11089"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 96934.5042551919,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017272089652139056",
            "extra": "mean: 10.3162440215032 usec\nrounds: 9407"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 61900.17096534245,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018758071489005949",
            "extra": "mean: 16.155044233397906 usec\nrounds: 11354"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 19218.54948826017,
            "unit": "iter/sec",
            "range": "stddev: 0.0000047227335204512764",
            "extra": "mean: 52.033063192977146 usec\nrounds: 6117"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37483.51075375225,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037000681379844512",
            "extra": "mean: 26.678397511094822 usec\nrounds: 11129"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23391.072209081995,
            "unit": "iter/sec",
            "range": "stddev: 0.000004922628313229139",
            "extra": "mean: 42.75135363874993 usec\nrounds: 7180"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16266.425965492534,
            "unit": "iter/sec",
            "range": "stddev: 0.000005432676361568456",
            "extra": "mean: 61.47631951366526 usec\nrounds: 637"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13102.62645840776,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061138986563318245",
            "extra": "mean: 76.32057612069944 usec\nrounds: 6014"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 78390.62882864186,
            "unit": "iter/sec",
            "range": "stddev: 0.000001653460019825322",
            "extra": "mean: 12.756626843572743 usec\nrounds: 16879"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 69774.52804705978,
            "unit": "iter/sec",
            "range": "stddev: 0.000001896445885841126",
            "extra": "mean: 14.331877663515616 usec\nrounds: 17250"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32695.799316439963,
            "unit": "iter/sec",
            "range": "stddev: 0.000003323397985308728",
            "extra": "mean: 30.58496873930787 usec\nrounds: 8586"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16233.738081702084,
            "unit": "iter/sec",
            "range": "stddev: 0.000005333539618816636",
            "extra": "mean: 61.60010682488179 usec\nrounds: 5515"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19605.574227259414,
            "unit": "iter/sec",
            "range": "stddev: 0.000005064880490077946",
            "extra": "mean: 51.00590211785834 usec\nrounds: 6697"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 22953.513399089894,
            "unit": "iter/sec",
            "range": "stddev: 0.000004597717881699092",
            "extra": "mean: 43.56631521341086 usec\nrounds: 7885"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77149.89822164999,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018616180733473395",
            "extra": "mean: 12.961779899268587 usec\nrounds: 19417"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 55227.16578397983,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020819797581131833",
            "extra": "mean: 18.107030947622476 usec\nrounds: 16076"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 63945.36599233335,
            "unit": "iter/sec",
            "range": "stddev: 0.000001943960995323959",
            "extra": "mean: 15.63834977690008 usec\nrounds: 17306"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 50722.525423911255,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024656346752854673",
            "extra": "mean: 19.715106683717824 usec\nrounds: 9497"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 24766.061190921264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000044494225194515196",
            "extra": "mean: 40.37783773087744 usec\nrounds: 6968"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22528.18655933387,
            "unit": "iter/sec",
            "range": "stddev: 0.000004560335153066833",
            "extra": "mean: 44.38883695171107 usec\nrounds: 6965"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 62635.19875760796,
            "unit": "iter/sec",
            "range": "stddev: 0.000002077223893613355",
            "extra": "mean: 15.965463826017404 usec\nrounds: 16814"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 48584.93562496064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026588903278631412",
            "extra": "mean: 20.582511577647278 usec\nrounds: 12770"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45671.9153181457,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027707938288323097",
            "extra": "mean: 21.895293705860734 usec\nrounds: 10447"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 45722.26924976834,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028981358285642012",
            "extra": "mean: 21.871180420579556 usec\nrounds: 13819"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 46049.122197297955,
            "unit": "iter/sec",
            "range": "stddev: 0.000002649532827695598",
            "extra": "mean: 21.715940549648035 usec\nrounds: 13389"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 46045.4894487386,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026518830890380385",
            "extra": "mean: 21.71765382390554 usec\nrounds: 13855"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 45817.46049310734,
            "unit": "iter/sec",
            "range": "stddev: 0.000002766314519231644",
            "extra": "mean: 21.82574043252435 usec\nrounds: 16863"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 45675.76098885539,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033394737385857303",
            "extra": "mean: 21.893450231600827 usec\nrounds: 14099"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 46120.01704495532,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025341416523725627",
            "extra": "mean: 21.682559202553062 usec\nrounds: 14165"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46118.93401375895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024543491342114818",
            "extra": "mean: 21.68306838362013 usec\nrounds: 14371"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 46012.30770687813,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026906575594269493",
            "extra": "mean: 21.733315493987178 usec\nrounds: 12061"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 31027.03170099396,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036359769991200683",
            "extra": "mean: 32.22996030161547 usec\nrounds: 10351"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41099.92940724015,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027723167968743706",
            "extra": "mean: 24.330942033779756 usec\nrounds: 12027"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 41277.455953997334,
            "unit": "iter/sec",
            "range": "stddev: 0.000003970118476317675",
            "extra": "mean: 24.226299244664553 usec\nrounds: 11058"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 62832.7696667532,
            "unit": "iter/sec",
            "range": "stddev: 0.00000219651919269379",
            "extra": "mean: 15.91526213636149 usec\nrounds: 17444"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 60087.55629622712,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023352735053436517",
            "extra": "mean: 16.642380912781263 usec\nrounds: 15149"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 64928.73423309236,
            "unit": "iter/sec",
            "range": "stddev: 0.000002487853799980351",
            "extra": "mean: 15.40150153566875 usec\nrounds: 11741"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 62021.594416239095,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019880916810638026",
            "extra": "mean: 16.123416519878603 usec\nrounds: 19045"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 51452.197724155754,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025604183073306225",
            "extra": "mean: 19.435515764772095 usec\nrounds: 13898"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 40992.22770014613,
            "unit": "iter/sec",
            "range": "stddev: 0.000002938011927828468",
            "extra": "mean: 24.394868395904112 usec\nrounds: 6644"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 45669.13935678919,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023316479399756936",
            "extra": "mean: 21.896624593415723 usec\nrounds: 13273"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26752.27205810218,
            "unit": "iter/sec",
            "range": "stddev: 0.000003911486733942721",
            "extra": "mean: 37.38000263409928 usec\nrounds: 6531"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24051.788674053332,
            "unit": "iter/sec",
            "range": "stddev: 0.000004585419804456979",
            "extra": "mean: 41.576949371702376 usec\nrounds: 7996"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 121760.05486906318,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011865536529070944",
            "extra": "mean: 8.212874091387095 usec\nrounds: 20758"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 97538.3496640773,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013469937166405435",
            "extra": "mean: 10.252377689842064 usec\nrounds: 24282"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 127312.93988669846,
            "unit": "iter/sec",
            "range": "stddev: 0.000001139439656857409",
            "extra": "mean: 7.854661127847219 usec\nrounds: 16186"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 158802.43524575766,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012780552375203692",
            "extra": "mean: 6.297132650720572 usec\nrounds: 35555"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 135919.85075663435,
            "unit": "iter/sec",
            "range": "stddev: 0.000001152690729522266",
            "extra": "mean: 7.357277060217706 usec\nrounds: 27992"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 151302.26802063052,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010400285927778724",
            "extra": "mean: 6.609286252494556 usec\nrounds: 32566"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 206772.73010872718,
            "unit": "iter/sec",
            "range": "stddev: 8.562346975965568e-7",
            "extra": "mean: 4.836227676029478 usec\nrounds: 34389"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 101814.60383450561,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013276159509568263",
            "extra": "mean: 9.821773717505678 usec\nrounds: 15317"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 136779.49065173414,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011824207714251095",
            "extra": "mean: 7.311037606845494 usec\nrounds: 27389"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 89563.75105380495,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015344306635558415",
            "extra": "mean: 11.165231337835047 usec\nrounds: 12760"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51816.99140711113,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024093756977526574",
            "extra": "mean: 19.298688959829587 usec\nrounds: 9700"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 334284.9472565833,
            "unit": "iter/sec",
            "range": "stddev: 6.485630905788447e-7",
            "extra": "mean: 2.9914598554521254 usec\nrounds: 27501"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 284501.68547064805,
            "unit": "iter/sec",
            "range": "stddev: 7.264741336710569e-7",
            "extra": "mean: 3.5149176650595613 usec\nrounds: 42978"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 357523.7945898046,
            "unit": "iter/sec",
            "range": "stddev: 5.832576625490469e-7",
            "extra": "mean: 2.7970166325497954 usec\nrounds: 45207"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 229044.19655670493,
            "unit": "iter/sec",
            "range": "stddev: 7.956013551004314e-7",
            "extra": "mean: 4.365969603392365 usec\nrounds: 40562"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 349849.7302116087,
            "unit": "iter/sec",
            "range": "stddev: 6.429943224973048e-7",
            "extra": "mean: 2.8583700761899804 usec\nrounds: 57261"
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
          "id": "c82712c82bcde087a1e2d3f701b40289625478db",
          "message": "Merge pull request #100 from amsdal/feature/postgres-c-dep\n\nAdjusted extra dep: [postgres-c]",
          "timestamp": "2025-06-16T19:15:57+03:00",
          "tree_id": "30cb477fb674a50fa0fa40156fe0df39ccb38771",
          "url": "https://github.com/amsdal/amsdal-glue/commit/c82712c82bcde087a1e2d3f701b40289625478db"
        },
        "date": 1750090589984,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 78869.74888548489,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017310208886508849",
            "extra": "mean: 12.679132546142021 usec\nrounds: 3864"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 54679.8335859792,
            "unit": "iter/sec",
            "range": "stddev: 0.000004765031338008353",
            "extra": "mean: 18.288278043633554 usec\nrounds: 16400"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 88476.92721746453,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018790867971751865",
            "extra": "mean: 11.30238166547232 usec\nrounds: 11793"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53610.214012703655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024215537668995456",
            "extra": "mean: 18.653161872531168 usec\nrounds: 9164"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 172853.44752853372,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010358286471821756",
            "extra": "mean: 5.78524764358504 usec\nrounds: 25370"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 72171.10017584387,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018087680582585019",
            "extra": "mean: 13.855961701616215 usec\nrounds: 10918"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 95729.16966782213,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018497335217728284",
            "extra": "mean: 10.446136778058094 usec\nrounds: 9437"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 61830.633633747246,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019604722868605687",
            "extra": "mean: 16.173212875732176 usec\nrounds: 11221"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 18761.893308285416,
            "unit": "iter/sec",
            "range": "stddev: 0.000006669329387022566",
            "extra": "mean: 53.29952492365956 usec\nrounds: 6235"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37564.79328339881,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035062643218786436",
            "extra": "mean: 26.620670915336433 usec\nrounds: 10593"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23284.996263373137,
            "unit": "iter/sec",
            "range": "stddev: 0.000004871227959955984",
            "extra": "mean: 42.94610953290044 usec\nrounds: 8151"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16274.561795223854,
            "unit": "iter/sec",
            "range": "stddev: 0.000006421605135498024",
            "extra": "mean: 61.44558683561441 usec\nrounds: 626"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 12993.230556266779,
            "unit": "iter/sec",
            "range": "stddev: 0.000006545906460469849",
            "extra": "mean: 76.96315367217808 usec\nrounds: 6517"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 77460.35737340325,
            "unit": "iter/sec",
            "range": "stddev: 0.000002370658454057584",
            "extra": "mean: 12.909829413507966 usec\nrounds: 17467"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 69928.6831914552,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018416472698264548",
            "extra": "mean: 14.300283579802818 usec\nrounds: 19245"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 32959.849833561,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035792839405631104",
            "extra": "mean: 30.339944054652854 usec\nrounds: 8225"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16282.43410430159,
            "unit": "iter/sec",
            "range": "stddev: 0.000005645090916607233",
            "extra": "mean: 61.415878829554984 usec\nrounds: 5350"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19568.599285615954,
            "unit": "iter/sec",
            "range": "stddev: 0.000004960015468266808",
            "extra": "mean: 51.10227796095031 usec\nrounds: 7496"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23097.930391423648,
            "unit": "iter/sec",
            "range": "stddev: 0.000004572542992490111",
            "extra": "mean: 43.293922141669626 usec\nrounds: 8183"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77553.53938897447,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017162864900924408",
            "extra": "mean: 12.894318014093972 usec\nrounds: 20600"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 55511.207818992814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021343925334231804",
            "extra": "mean: 18.014380145730794 usec\nrounds: 17686"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64657.01511734174,
            "unit": "iter/sec",
            "range": "stddev: 0.000001939219794985445",
            "extra": "mean: 15.466225871781525 usec\nrounds: 19349"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 50363.658156196194,
            "unit": "iter/sec",
            "range": "stddev: 0.000002331803699388539",
            "extra": "mean: 19.85558707627299 usec\nrounds: 13929"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 24609.318828679017,
            "unit": "iter/sec",
            "range": "stddev: 0.000004056312032137367",
            "extra": "mean: 40.635013385036395 usec\nrounds: 7020"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22635.791921615604,
            "unit": "iter/sec",
            "range": "stddev: 0.000004453842036073343",
            "extra": "mean: 44.1778226033731 usec\nrounds: 6535"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 62758.60485713684,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021359088080157065",
            "extra": "mean: 15.934069953855598 usec\nrounds: 16021"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 49129.63604986297,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024288803855127176",
            "extra": "mean: 20.354313208937135 usec\nrounds: 11929"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45639.30258128354,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027180369081037604",
            "extra": "mean: 21.9109395508181 usec\nrounds: 10601"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 45809.18014995267,
            "unit": "iter/sec",
            "range": "stddev: 0.000002737733915945246",
            "extra": "mean: 21.829685594166506 usec\nrounds: 13281"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 45901.09308724419,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026622166960216113",
            "extra": "mean: 21.78597355185639 usec\nrounds: 13981"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 45824.590923746546,
            "unit": "iter/sec",
            "range": "stddev: 0.000002550048143673546",
            "extra": "mean: 21.82234428811441 usec\nrounds: 13543"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 45874.0148479916,
            "unit": "iter/sec",
            "range": "stddev: 0.00000260279786635494",
            "extra": "mean: 21.79883324608944 usec\nrounds: 11581"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 45751.049262428525,
            "unit": "iter/sec",
            "range": "stddev: 0.00000306725553676672",
            "extra": "mean: 21.857422203892835 usec\nrounds: 10583"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 45528.38630382546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029083469547112646",
            "extra": "mean: 21.96431899269789 usec\nrounds: 14613"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46068.402034757564,
            "unit": "iter/sec",
            "range": "stddev: 0.000002589849300813687",
            "extra": "mean: 21.706852328967756 usec\nrounds: 14272"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 46042.59856275821,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029993038778389576",
            "extra": "mean: 21.719017414643815 usec\nrounds: 11753"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 30735.83499354537,
            "unit": "iter/sec",
            "range": "stddev: 0.000003581051224341786",
            "extra": "mean: 32.535312615063276 usec\nrounds: 9899"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41090.10936782617,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028059034597330253",
            "extra": "mean: 24.336756834797008 usec\nrounds: 13247"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 41819.63226029328,
            "unit": "iter/sec",
            "range": "stddev: 0.000003106537069441207",
            "extra": "mean: 23.91221409542321 usec\nrounds: 12168"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 61247.909025262954,
            "unit": "iter/sec",
            "range": "stddev: 0.000002772850165112309",
            "extra": "mean: 16.327087992302392 usec\nrounds: 16429"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 59182.1043497079,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021106979223958543",
            "extra": "mean: 16.89699970942205 usec\nrounds: 15306"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 64622.87994811418,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018903080898748505",
            "extra": "mean: 15.474395458743123 usec\nrounds: 10526"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 61137.2321977983,
            "unit": "iter/sec",
            "range": "stddev: 0.000002190678581243804",
            "extra": "mean: 16.356644945336804 usec\nrounds: 16577"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 51403.684781693366,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022889690731244617",
            "extra": "mean: 19.453858303094542 usec\nrounds: 14574"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41467.398807821264,
            "unit": "iter/sec",
            "range": "stddev: 0.000002304923580409823",
            "extra": "mean: 24.11532984343806 usec\nrounds: 7027"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 44627.35306685307,
            "unit": "iter/sec",
            "range": "stddev: 0.000003714705817078187",
            "extra": "mean: 22.407782027806377 usec\nrounds: 14310"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26950.460825530194,
            "unit": "iter/sec",
            "range": "stddev: 0.000004333819202437138",
            "extra": "mean: 37.10511692077262 usec\nrounds: 6739"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24338.340069419053,
            "unit": "iter/sec",
            "range": "stddev: 0.000004512171410432634",
            "extra": "mean: 41.08743641299074 usec\nrounds: 8407"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 122439.23560049006,
            "unit": "iter/sec",
            "range": "stddev: 0.000001174412142608591",
            "extra": "mean: 8.167316588474337 usec\nrounds: 22967"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 98711.5513177054,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014321780180819474",
            "extra": "mean: 10.130526636963461 usec\nrounds: 27470"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 116444.17321618214,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013343683406737686",
            "extra": "mean: 8.587806262692679 usec\nrounds: 17093"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 141893.57463850215,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010533533907604692",
            "extra": "mean: 7.047535468379515 usec\nrounds: 33178"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 130578.18923051264,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010781880954359516",
            "extra": "mean: 7.658246801345033 usec\nrounds: 27597"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 153714.10729946147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010191919977245405",
            "extra": "mean: 6.5055837591524925 usec\nrounds: 33330"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 208219.13256955048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010099273122819773",
            "extra": "mean: 4.802632628708961 usec\nrounds: 33330"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 101473.9975165985,
            "unit": "iter/sec",
            "range": "stddev: 0.000001301292628500641",
            "extra": "mean: 9.854741357128718 usec\nrounds: 18332"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 135900.27822233393,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017643612226367565",
            "extra": "mean: 7.358336664800584 usec\nrounds: 30584"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 88481.86369092956,
            "unit": "iter/sec",
            "range": "stddev: 0.000001567571792298464",
            "extra": "mean: 11.301751096620627 usec\nrounds: 14100"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52418.972655879385,
            "unit": "iter/sec",
            "range": "stddev: 0.000002503464974624972",
            "extra": "mean: 19.07706216535014 usec\nrounds: 8101"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 340621.56444930355,
            "unit": "iter/sec",
            "range": "stddev: 6.522120084548141e-7",
            "extra": "mean: 2.935809427147514 usec\nrounds: 42725"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 291843.2857314081,
            "unit": "iter/sec",
            "range": "stddev: 7.095890391921438e-7",
            "extra": "mean: 3.4264965099122726 usec\nrounds: 44429"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 370187.30184531905,
            "unit": "iter/sec",
            "range": "stddev: 5.824454670907675e-7",
            "extra": "mean: 2.7013352295315767 usec\nrounds: 46864"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 226617.81058762758,
            "unit": "iter/sec",
            "range": "stddev: 8.162426542259911e-7",
            "extra": "mean: 4.412715829382371 usec\nrounds: 45413"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 378274.6282027226,
            "unit": "iter/sec",
            "range": "stddev: 5.626809197840783e-7",
            "extra": "mean: 2.6435820048287413 usec\nrounds: 59600"
          }
        ]
      },
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
          "id": "26d64d04730d73e2f03c855b8bf951b3fc3fb73c",
          "message": "Merge pull request #101 from amsdal/feature/uv-version-update\n\nUpdate package manager to uv",
          "timestamp": "2025-06-17T16:10:22+03:00",
          "tree_id": "1e49d60d9a6407fd05cbea7ad1a880f9bc0dc52e",
          "url": "https://github.com/amsdal/amsdal-glue/commit/26d64d04730d73e2f03c855b8bf951b3fc3fb73c"
        },
        "date": 1750165881779,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 78186.43647632931,
            "unit": "iter/sec",
            "range": "stddev: 0.000001727196141786081",
            "extra": "mean: 12.789942157074096 usec\nrounds: 3924"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 60888.647213887925,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019675874350845816",
            "extra": "mean: 16.423422850687224 usec\nrounds: 15461"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 88857.22476550673,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014592935114138974",
            "extra": "mean: 11.254008918678132 usec\nrounds: 12568"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 52843.08764753119,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026791969540306747",
            "extra": "mean: 18.923950974820066 usec\nrounds: 9581"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 172163.81682247345,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011765446039998949",
            "extra": "mean: 5.808421411980829 usec\nrounds: 23957"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 72025.5254276544,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018347592196931116",
            "extra": "mean: 13.883966747378246 usec\nrounds: 11184"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 98291.9753485993,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014263201539838846",
            "extra": "mean: 10.17377050825798 usec\nrounds: 11025"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 61453.36507161755,
            "unit": "iter/sec",
            "range": "stddev: 0.000002227632559031119",
            "extra": "mean: 16.272501901801526 usec\nrounds: 11677"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 19409.874841019355,
            "unit": "iter/sec",
            "range": "stddev: 0.000004570964411399613",
            "extra": "mean: 51.52016734732756 usec\nrounds: 6235"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 38472.9310667413,
            "unit": "iter/sec",
            "range": "stddev: 0.000003171478478709988",
            "extra": "mean: 25.99230087942195 usec\nrounds: 10751"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23554.071934909516,
            "unit": "iter/sec",
            "range": "stddev: 0.000004357604420441969",
            "extra": "mean: 42.45550420171295 usec\nrounds: 8167"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16552.420027318632,
            "unit": "iter/sec",
            "range": "stddev: 0.00000603151229815911",
            "extra": "mean: 60.41412665637827 usec\nrounds: 613"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13137.863509181134,
            "unit": "iter/sec",
            "range": "stddev: 0.00000594493932319933",
            "extra": "mean: 76.11587677868398 usec\nrounds: 6527"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 78991.10222948984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017041714749828534",
            "extra": "mean: 12.65965370497981 usec\nrounds: 14134"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 71157.27563908052,
            "unit": "iter/sec",
            "range": "stddev: 0.000001859599062887268",
            "extra": "mean: 14.05337670700235 usec\nrounds: 19744"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33305.441226618874,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033404218097413267",
            "extra": "mean: 30.025123918813748 usec\nrounds: 7509"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16035.585024311782,
            "unit": "iter/sec",
            "range": "stddev: 0.000009487148410746228",
            "extra": "mean: 62.36130446652776 usec\nrounds: 5541"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 19875.815525863465,
            "unit": "iter/sec",
            "range": "stddev: 0.000005001797256273478",
            "extra": "mean: 50.31240095274314 usec\nrounds: 7748"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23254.220735992105,
            "unit": "iter/sec",
            "range": "stddev: 0.000004340587132467193",
            "extra": "mean: 43.002946060980385 usec\nrounds: 7904"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 76872.88770732527,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017530974609962735",
            "extra": "mean: 13.008487515224555 usec\nrounds: 22743"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 55795.138811867604,
            "unit": "iter/sec",
            "range": "stddev: 0.000002193065199555826",
            "extra": "mean: 17.922708345109456 usec\nrounds: 16728"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64955.99405558694,
            "unit": "iter/sec",
            "range": "stddev: 0.000001843175868437901",
            "extra": "mean: 15.39503804905575 usec\nrounds: 19444"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 51217.311860152055,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023247332983391594",
            "extra": "mean: 19.5246482816295 usec\nrounds: 14991"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 25160.187208340492,
            "unit": "iter/sec",
            "range": "stddev: 0.000004183002978772453",
            "extra": "mean: 39.74533224730953 usec\nrounds: 7094"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22629.612791959462,
            "unit": "iter/sec",
            "range": "stddev: 0.000004968721325213179",
            "extra": "mean: 44.1898855801594 usec\nrounds: 8714"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 62729.942875748085,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019230425040964716",
            "extra": "mean: 15.941350400728776 usec\nrounds: 16337"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 49662.63144007538,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027262434936123552",
            "extra": "mean: 20.135864149821256 usec\nrounds: 11041"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 46023.44318735573,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026901051151048113",
            "extra": "mean: 21.72805706711521 usec\nrounds: 12329"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 46214.338144947484,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024885648716238448",
            "extra": "mean: 21.638306208423497 usec\nrounds: 13721"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 46150.462000140426,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026972481680949507",
            "extra": "mean: 21.668255455318242 usec\nrounds: 14643"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 45207.28103737247,
            "unit": "iter/sec",
            "range": "stddev: 0.000003476074365000607",
            "extra": "mean: 22.120330554127083 usec\nrounds: 12834"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 46299.965460951935,
            "unit": "iter/sec",
            "range": "stddev: 0.000002437102790135663",
            "extra": "mean: 21.59828825020121 usec\nrounds: 13787"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 46385.86204346987,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025664411942825645",
            "extra": "mean: 21.558292892408982 usec\nrounds: 14141"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 45826.01634012187,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024973511304744744",
            "extra": "mean: 21.821665504982462 usec\nrounds: 15841"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46322.39939905247,
            "unit": "iter/sec",
            "range": "stddev: 0.000002574985971914219",
            "extra": "mean: 21.587828199168268 usec\nrounds: 13969"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 46326.00850900337,
            "unit": "iter/sec",
            "range": "stddev: 0.000002791197044478237",
            "extra": "mean: 21.586146361080342 usec\nrounds: 9492"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 31427.75714746337,
            "unit": "iter/sec",
            "range": "stddev: 0.00000364228035509732",
            "extra": "mean: 31.819006215043036 usec\nrounds: 8794"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41868.07802100066,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027495246534720147",
            "extra": "mean: 23.884545153909592 usec\nrounds: 12030"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 42452.487372893556,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028667929125026297",
            "extra": "mean: 23.555745773297435 usec\nrounds: 12718"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 62792.579546664194,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021591037472342727",
            "extra": "mean: 15.925448631344278 usec\nrounds: 14688"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 60989.212814109604,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021178826243440243",
            "extra": "mean: 16.39634213755017 usec\nrounds: 16130"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 64103.35753887776,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019764534826447103",
            "extra": "mean: 15.59980691172868 usec\nrounds: 10828"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 61249.683533560725,
            "unit": "iter/sec",
            "range": "stddev: 0.000001971599962979946",
            "extra": "mean: 16.32661496858293 usec\nrounds: 16795"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 52591.69897335009,
            "unit": "iter/sec",
            "range": "stddev: 0.00000245084433292312",
            "extra": "mean: 19.01440758753073 usec\nrounds: 13728"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 41774.74057212161,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025722495426506696",
            "extra": "mean: 23.937910476632627 usec\nrounds: 7858"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46126.053377625365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022164666879203625",
            "extra": "mean: 21.679721692493114 usec\nrounds: 12545"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 26953.270321564672,
            "unit": "iter/sec",
            "range": "stddev: 0.000003948289923084566",
            "extra": "mean: 37.10124923875838 usec\nrounds: 6600"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24283.22311062649,
            "unit": "iter/sec",
            "range": "stddev: 0.00000436046266008892",
            "extra": "mean: 41.18069481321834 usec\nrounds: 9621"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 122541.12567185114,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011823819750272485",
            "extra": "mean: 8.160525656324289 usec\nrounds: 22116"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 99110.549875479,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012714877143557614",
            "extra": "mean: 10.089743233756495 usec\nrounds: 26217"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 123848.49297942992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012240483549265064",
            "extra": "mean: 8.074381657321341 usec\nrounds: 16144"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 143486.58669146767,
            "unit": "iter/sec",
            "range": "stddev: 0.00000123701720674577",
            "extra": "mean: 6.969292552412944 usec\nrounds: 33459"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 137642.1672264142,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010525930452258306",
            "extra": "mean: 7.265215450691445 usec\nrounds: 27980"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 147888.59242902987,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010377217050934348",
            "extra": "mean: 6.761846762994171 usec\nrounds: 32164"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 207781.04695009938,
            "unit": "iter/sec",
            "range": "stddev: 8.172249882591175e-7",
            "extra": "mean: 4.812758500731588 usec\nrounds: 30973"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 101660.3472545961,
            "unit": "iter/sec",
            "range": "stddev: 0.000001310405539466285",
            "extra": "mean: 9.836677003430063 usec\nrounds: 16813"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137940.25976864508,
            "unit": "iter/sec",
            "range": "stddev: 0.000001160857023869261",
            "extra": "mean: 7.2495151283404216 usec\nrounds: 33421"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 89609.42855179182,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014198697507174413",
            "extra": "mean: 11.15953997432343 usec\nrounds: 13085"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 51694.40302989384,
            "unit": "iter/sec",
            "range": "stddev: 0.000002788898605722762",
            "extra": "mean: 19.344453971578314 usec\nrounds: 9742"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 341174.48057675327,
            "unit": "iter/sec",
            "range": "stddev: 6.212143223571234e-7",
            "extra": "mean: 2.9310515789736282 usec\nrounds: 49868"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 292917.5418260325,
            "unit": "iter/sec",
            "range": "stddev: 6.672361387383955e-7",
            "extra": "mean: 3.413930056104024 usec\nrounds: 44466"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 371024.02766393084,
            "unit": "iter/sec",
            "range": "stddev: 5.743574471008986e-7",
            "extra": "mean: 2.6952432334268877 usec\nrounds: 42909"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 224887.5210077721,
            "unit": "iter/sec",
            "range": "stddev: 7.528637030398965e-7",
            "extra": "mean: 4.446667362950032 usec\nrounds: 44297"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 374826.1049525177,
            "unit": "iter/sec",
            "range": "stddev: 5.792190604936826e-7",
            "extra": "mean: 2.6679038273673017 usec\nrounds: 59376"
          }
        ]
      },
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
          "id": "3df2a27c5a549e01b9e350c710707cf375a4337a",
          "message": "Merge pull request #102 from amsdal/feature/pgvector\n\nVector operations",
          "timestamp": "2025-06-26T23:14:44+03:00",
          "tree_id": "eb3bf637f8554a0bb911683e534473d65fd845be",
          "url": "https://github.com/amsdal/amsdal-glue/commit/3df2a27c5a549e01b9e350c710707cf375a4337a"
        },
        "date": 1750968916432,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_data_mutations.py::test_simple_insert_command",
            "value": 77996.8170885499,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020803310009827145",
            "extra": "mean: 12.821036002849944 usec\nrounds: 3933"
          },
          {
            "name": "tests/test_data_mutations.py::test_multiple_inserts",
            "value": 61492.126027862236,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021255741511093985",
            "extra": "mean: 16.262244690432357 usec\nrounds: 16826"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command",
            "value": 89618.37733329926,
            "unit": "iter/sec",
            "range": "stddev: 0.000001610665257146598",
            "extra": "mean: 11.158425646125071 usec\nrounds: 14394"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_update_command_condition",
            "value": 53137.14673621185,
            "unit": "iter/sec",
            "range": "stddev: 0.000002587678999207871",
            "extra": "mean: 18.81922650014102 usec\nrounds: 7969"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command",
            "value": 176500.5013571126,
            "unit": "iter/sec",
            "range": "stddev: 9.87895900235571e-7",
            "extra": "mean: 5.665706285880202 usec\nrounds: 27406"
          },
          {
            "name": "tests/test_data_mutations.py::test_simple_delete_command_condition",
            "value": 73185.30463020205,
            "unit": "iter/sec",
            "range": "stddev: 0.00000191618745973282",
            "extra": "mean: 13.6639453105087 usec\nrounds: 11269"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_command",
            "value": 92975.87667622548,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024702759231837755",
            "extra": "mean: 10.755478041711289 usec\nrounds: 9258"
          },
          {
            "name": "tests/test_query_command.py::test_only_select_query_command",
            "value": 62429.35032147287,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023180225690986697",
            "extra": "mean: 16.018106785520164 usec\nrounds: 11655"
          },
          {
            "name": "tests/test_query_command.py::test_conditions",
            "value": 19419.657276532496,
            "unit": "iter/sec",
            "range": "stddev: 0.000004896034013682474",
            "extra": "mean: 51.49421463830058 usec\nrounds: 5653"
          },
          {
            "name": "tests/test_query_command.py::test_simple_alias",
            "value": 37687.39535604717,
            "unit": "iter/sec",
            "range": "stddev: 0.000004156913165767988",
            "extra": "mean: 26.53407035834181 usec\nrounds: 11804"
          },
          {
            "name": "tests/test_query_command.py::test_simple_join",
            "value": 23246.401571014983,
            "unit": "iter/sec",
            "range": "stddev: 0.0000054237940303656855",
            "extra": "mean: 43.017410541804466 usec\nrounds: 8066"
          },
          {
            "name": "tests/test_query_command.py::test_multiple_joins",
            "value": 16603.38680190144,
            "unit": "iter/sec",
            "range": "stddev: 0.0000067873211671203604",
            "extra": "mean: 60.22867574737696 usec\nrounds: 623"
          },
          {
            "name": "tests/test_query_command.py::test_query_ordering",
            "value": 13213.940828291123,
            "unit": "iter/sec",
            "range": "stddev: 0.000006404844584219152",
            "extra": "mean: 75.67765082306062 usec\nrounds: 6483"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit",
            "value": 79794.42641573501,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018183106346555758",
            "extra": "mean: 12.532203625224701 usec\nrounds: 16493"
          },
          {
            "name": "tests/test_query_command.py::test_simple_query_limit_offset",
            "value": 71090.26056354106,
            "unit": "iter/sec",
            "range": "stddev: 0.000002028558881367769",
            "extra": "mean: 14.066624486573541 usec\nrounds: 19593"
          },
          {
            "name": "tests/test_query_command.py::test_simple_group_by",
            "value": 33707.19590090335,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035158991498938636",
            "extra": "mean: 29.66725570824478 usec\nrounds: 8937"
          },
          {
            "name": "tests/test_query_command.py::test_simple_aggregate",
            "value": 16712.190073093505,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052451560691145874",
            "extra": "mean: 59.83656215171895 usec\nrounds: 5674"
          },
          {
            "name": "tests/test_query_command.py::test_aggregation_with_joins",
            "value": 20029.84927744369,
            "unit": "iter/sec",
            "range": "stddev: 0.000004811684935913053",
            "extra": "mean: 49.92548801283966 usec\nrounds: 7048"
          },
          {
            "name": "tests/test_query_command.py::test_simple_annotation",
            "value": 23543.042498713334,
            "unit": "iter/sec",
            "range": "stddev: 0.000004317389916073732",
            "extra": "mean: 42.47539374125717 usec\nrounds: 8473"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_single_field",
            "value": 77649.47870920235,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018134227222409704",
            "extra": "mean: 12.878386521370023 usec\nrounds: 19475"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on",
            "value": 54467.424819016385,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028209710353024948",
            "extra": "mean: 18.35959756354897 usec\nrounds: 12863"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_multiple_fields",
            "value": 64138.56290665464,
            "unit": "iter/sec",
            "range": "stddev: 0.000001987996568589423",
            "extra": "mean: 15.591244248103443 usec\nrounds: 22788"
          },
          {
            "name": "tests/test_query_command.py::test_select_distinct_on_multiple_fields",
            "value": 50088.42272993052,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024368902978630997",
            "extra": "mean: 19.964693346241994 usec\nrounds: 17071"
          },
          {
            "name": "tests/test_query_command.py::test_join_subquery_simple",
            "value": 24730.392247095646,
            "unit": "iter/sec",
            "range": "stddev: 0.000004312818822538127",
            "extra": "mean: 40.43607517456342 usec\nrounds: 7588"
          },
          {
            "name": "tests/test_query_command.py::test_from_subquery",
            "value": 22362.0438403623,
            "unit": "iter/sec",
            "range": "stddev: 0.000004597722987451233",
            "extra": "mean: 44.718631585680605 usec\nrounds: 8225"
          },
          {
            "name": "tests/test_query_command.py::test_select_aliased_query",
            "value": 62167.760787117906,
            "unit": "iter/sec",
            "range": "stddev: 0.000002077593269508976",
            "extra": "mean: 16.085507783114732 usec\nrounds: 14852"
          },
          {
            "name": "tests/test_query_command.py::test_select_aggregation_aliased_query",
            "value": 49226.03935694439,
            "unit": "iter/sec",
            "range": "stddev: 0.000002565358095649464",
            "extra": "mean: 20.314451722367313 usec\nrounds: 11930"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[---]",
            "value": 45871.349018872075,
            "unit": "iter/sec",
            "range": "stddev: 0.000002985514388010507",
            "extra": "mean: 21.8001000927308 usec\nrounds: 11323"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[+-+]",
            "value": 45721.15629276717,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026520154858638698",
            "extra": "mean: 21.87171281488772 usec\nrounds: 13219"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[/-/]",
            "value": 45853.476050644786,
            "unit": "iter/sec",
            "range": "stddev: 0.00000303729528404198",
            "extra": "mean: 21.808597430988836 usec\nrounds: 13566"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[*-*]",
            "value": 46078.16805106848,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024783150241085082",
            "extra": "mean: 21.70225168005158 usec\nrounds: 15238"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[%-%]",
            "value": 46144.17450125852,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024859154281663575",
            "extra": "mean: 21.671207921873783 usec\nrounds: 12677"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[^-^]",
            "value": 46111.96744964248,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025828067931681115",
            "extra": "mean: 21.686344246579168 usec\nrounds: 14816"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[&-&]",
            "value": 46118.97789355747,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025178439198354375",
            "extra": "mean: 21.683047753313147 usec\nrounds: 15561"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression[|-|]",
            "value": 46251.37983549623,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025050511570667493",
            "extra": "mean: 21.62097657533099 usec\nrounds: 15022"
          },
          {
            "name": "tests/test_query_command.py::test_select_math_expression_mixed",
            "value": 46361.77186531274,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028925566396299854",
            "extra": "mean: 21.56949486109237 usec\nrounds: 11461"
          },
          {
            "name": "tests/test_query_command.py::test_complex_math_mixed",
            "value": 31284.36537073378,
            "unit": "iter/sec",
            "range": "stddev: 0.000003541041964678279",
            "extra": "mean: 31.96484851616937 usec\nrounds: 10285"
          },
          {
            "name": "tests/test_query_command.py::test_select_pow_expression",
            "value": 41874.82878358992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027053145494497604",
            "extra": "mean: 23.88069465711784 usec\nrounds: 12353"
          },
          {
            "name": "tests/test_query_command.py::test_select_power_mixed",
            "value": 42792.27832220887,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027740114276768476",
            "extra": "mean: 23.368701999701837 usec\nrounds: 12603"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[10-10]",
            "value": 64081.941834982485,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028697563647981174",
            "extra": "mean: 15.605020250090138 usec\nrounds: 13210"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[20.5-20.5]",
            "value": 60502.57692492076,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021536556470150124",
            "extra": "mean: 16.528221620062997 usec\nrounds: 15153"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression['Hello'-Hello]",
            "value": 66009.00840313535,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019666482775171306",
            "extra": "mean: 15.149447388949131 usec\nrounds: 10533"
          },
          {
            "name": "tests/test_query_command.py::test_select_value_expression[TRUE-True]",
            "value": 62989.555276287356,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021338346919335455",
            "extra": "mean: 15.875647885014574 usec\nrounds: 13494"
          },
          {
            "name": "tests/test_query_command.py::test_select_nested_value_expression",
            "value": 52414.55313033428,
            "unit": "iter/sec",
            "range": "stddev: 0.000002428427243338011",
            "extra": "mean: 19.078670717909112 usec\nrounds: 14701"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_command",
            "value": 42610.288087764304,
            "unit": "iter/sec",
            "range": "stddev: 0.00000255011206739217",
            "extra": "mean: 23.468510654992578 usec\nrounds: 7403"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_primary_key",
            "value": 46912.227646848594,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023984365337777114",
            "extra": "mean: 21.31640406266609 usec\nrounds: 13135"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_constraints",
            "value": 27147.156548917927,
            "unit": "iter/sec",
            "range": "stddev: 0.000004090459853792724",
            "extra": "mean: 36.8362704284718 usec\nrounds: 6706"
          },
          {
            "name": "tests/test_schema_operations.py::test_simple_create_table_explicit_named_constraints",
            "value": 24804.58109500453,
            "unit": "iter/sec",
            "range": "stddev: 0.000004309782021878168",
            "extra": "mean: 40.31513357028203 usec\nrounds: 8523"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index",
            "value": 125704.56828686131,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011590018997348297",
            "extra": "mean: 7.955160370289584 usec\nrounds: 21201"
          },
          {
            "name": "tests/test_schema_operations.py::test_create_index_multi_column",
            "value": 100699.62394366755,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014377857109005062",
            "extra": "mean: 9.930523678612849 usec\nrounds: 25387"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_add_property",
            "value": 130523.59839997548,
            "unit": "iter/sec",
            "range": "stddev: 0.000001306020159948593",
            "extra": "mean: 7.6614498240816795 usec\nrounds: 16244"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_drop_property",
            "value": 151537.35761035196,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011108082254640028",
            "extra": "mean: 6.5990328442396375 usec\nrounds: 29255"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_property",
            "value": 138740.0066956162,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011597507736303856",
            "extra": "mean: 7.207726335158071 usec\nrounds: 30756"
          },
          {
            "name": "tests/test_schema_operations.py::test_update_schema_rename_table",
            "value": 147755.28392547416,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010568145279003808",
            "extra": "mean: 6.767947469847419 usec\nrounds: 30926"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_schema",
            "value": 207523.32918174838,
            "unit": "iter/sec",
            "range": "stddev: 9.442296982704424e-7",
            "extra": "mean: 4.818735339023993 usec\nrounds: 32444"
          },
          {
            "name": "tests/test_schema_operations.py::test_add_pk_constraint",
            "value": 103095.13001649959,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014667486977819145",
            "extra": "mean: 9.699779221772722 usec\nrounds: 17379"
          },
          {
            "name": "tests/test_schema_operations.py::test_delete_constraint",
            "value": 137771.67015322874,
            "unit": "iter/sec",
            "range": "stddev: 0.000001266728972426246",
            "extra": "mean: 7.25838627700315 usec\nrounds: 29623"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas",
            "value": 90418.42957805394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014902986573757722",
            "extra": "mean: 11.059692196232488 usec\nrounds: 13508"
          },
          {
            "name": "tests/test_schema_operations.py::test_fetch_schemas_conditions",
            "value": 52678.93054826123,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026446620169047457",
            "extra": "mean: 18.982921437326084 usec\nrounds: 9568"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_command",
            "value": 338055.143479204,
            "unit": "iter/sec",
            "range": "stddev: 8.166016560948453e-7",
            "extra": "mean: 2.958097278769896 usec\nrounds: 42841"
          },
          {
            "name": "tests/test_transaction_operations.py::test_begin_nested_transaction_command",
            "value": 295730.12944145565,
            "unit": "iter/sec",
            "range": "stddev: 7.524842593804162e-7",
            "extra": "mean: 3.3814613407456866 usec\nrounds: 41317"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_transaction_command",
            "value": 376915.25011601916,
            "unit": "iter/sec",
            "range": "stddev: 6.233987783360173e-7",
            "extra": "mean: 2.6531163164456406 usec\nrounds: 47478"
          },
          {
            "name": "tests/test_transaction_operations.py::test_rollback_nested_transaction_command",
            "value": 230016.6691065217,
            "unit": "iter/sec",
            "range": "stddev: 8.898972427644819e-7",
            "extra": "mean: 4.347511003808579 usec\nrounds: 42684"
          },
          {
            "name": "tests/test_transaction_operations.py::test_commit_transaction",
            "value": 355472.929998316,
            "unit": "iter/sec",
            "range": "stddev: 6.239810103594996e-7",
            "extra": "mean: 2.813153732985343 usec\nrounds: 57042"
          }
        ]
      }
    ]
  }
}