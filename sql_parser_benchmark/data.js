window.BENCHMARK_DATA = {
  "lastUpdate": 1721748073350,
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
      }
    ]
  }
}