window.BENCHMARK_DATA = {
  "lastUpdate": 1721910523522,
  "repoUrl": "https://github.com/amsdal/amsdal-glue",
  "entries": {
    "Connections Benchmark": [
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
        "date": 1721748114394,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 14932.350588518677,
            "unit": "iter/sec",
            "range": "stddev: 0.0004387584761539383",
            "extra": "mean: 66.96869284390424 usec\nrounds: 2740"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4849.59554299711,
            "unit": "iter/sec",
            "range": "stddev: 0.0008263379790509849",
            "extra": "mean: 206.2027629178304 usec\nrounds: 2210"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 5853.05957056895,
            "unit": "iter/sec",
            "range": "stddev: 0.002343091023958274",
            "extra": "mean: 170.8508153630144 usec\nrounds: 2438"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 12028.571223971503,
            "unit": "iter/sec",
            "range": "stddev: 0.0008324930448025541",
            "extra": "mean: 83.13539333808156 usec\nrounds: 3443"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 14259.020188655337,
            "unit": "iter/sec",
            "range": "stddev: 0.00014160689103599787",
            "extra": "mean: 70.13104594631355 usec\nrounds: 3588"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 6279.537628104478,
            "unit": "iter/sec",
            "range": "stddev: 0.0010920635078956677",
            "extra": "mean: 159.24739355401508 usec\nrounds: 3392"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 12938.865108367947,
            "unit": "iter/sec",
            "range": "stddev: 0.000686371626061497",
            "extra": "mean: 77.28653105389206 usec\nrounds: 2717"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 10452.370587858673,
            "unit": "iter/sec",
            "range": "stddev: 0.00009743575731477043",
            "extra": "mean: 95.67207664465953 usec\nrounds: 486"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 6429.0986180416385,
            "unit": "iter/sec",
            "range": "stddev: 0.0007738435107141521",
            "extra": "mean: 155.54279991813362 usec\nrounds: 3564"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 6877.683895592542,
            "unit": "iter/sec",
            "range": "stddev: 0.0008629155389739635",
            "extra": "mean: 145.3977843676175 usec\nrounds: 3097"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 8134.442159559345,
            "unit": "iter/sec",
            "range": "stddev: 0.000779072934007033",
            "extra": "mean: 122.93405993732846 usec\nrounds: 3854"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 7073.368791831897,
            "unit": "iter/sec",
            "range": "stddev: 0.00018891492205522526",
            "extra": "mean: 141.37535160824197 usec\nrounds: 2324"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 5342.609629852759,
            "unit": "iter/sec",
            "range": "stddev: 0.0014770976019791169",
            "extra": "mean: 187.17444643762224 usec\nrounds: 2736"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 13679.933882820998,
            "unit": "iter/sec",
            "range": "stddev: 0.001382195163607279",
            "extra": "mean: 73.099768505152 usec\nrounds: 4345"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 11661.695519470779,
            "unit": "iter/sec",
            "range": "stddev: 0.001351939653794626",
            "extra": "mean: 85.75082399727935 usec\nrounds: 3980"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 10898.178107724898,
            "unit": "iter/sec",
            "range": "stddev: 0.0010271608533155452",
            "extra": "mean: 91.75845633236398 usec\nrounds: 3040"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 16503.528968155137,
            "unit": "iter/sec",
            "range": "stddev: 0.0006976974038864186",
            "extra": "mean: 60.593101143978295 usec\nrounds: 3796"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 10766.379808300837,
            "unit": "iter/sec",
            "range": "stddev: 0.0018357327674593255",
            "extra": "mean: 92.88173163174162 usec\nrounds: 4068"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 12839.943881629244,
            "unit": "iter/sec",
            "range": "stddev: 0.0013272931189691748",
            "extra": "mean: 77.88196032778231 usec\nrounds: 3826"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 21856.093303180387,
            "unit": "iter/sec",
            "range": "stddev: 0.00005650433654170533",
            "extra": "mean: 45.753831031389545 usec\nrounds: 2693"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 12467.284349193274,
            "unit": "iter/sec",
            "range": "stddev: 0.0014022868695419159",
            "extra": "mean: 80.20992960385213 usec\nrounds: 3352"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 15960.33633112997,
            "unit": "iter/sec",
            "range": "stddev: 0.0008930074085130142",
            "extra": "mean: 62.65532124467464 usec\nrounds: 4015"
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
        "date": 1721910522746,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 17092.737280581307,
            "unit": "iter/sec",
            "range": "stddev: 0.00007299879214603687",
            "extra": "mean: 58.50438016946991 usec\nrounds: 1602"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4946.2559425562085,
            "unit": "iter/sec",
            "range": "stddev: 0.0009930046429207063",
            "extra": "mean: 202.17312076317737 usec\nrounds: 2887"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 7148.669174172909,
            "unit": "iter/sec",
            "range": "stddev: 0.0010756710413892892",
            "extra": "mean: 139.88617680236945 usec\nrounds: 3246"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 8547.619630956075,
            "unit": "iter/sec",
            "range": "stddev: 0.0020085713676189173",
            "extra": "mean: 116.9916354698796 usec\nrounds: 2284"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 12410.464571747842,
            "unit": "iter/sec",
            "range": "stddev: 0.0005928892910700806",
            "extra": "mean: 80.57716084831173 usec\nrounds: 3935"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 8225.310797634167,
            "unit": "iter/sec",
            "range": "stddev: 0.0009095711891338139",
            "extra": "mean: 121.5759531284372 usec\nrounds: 2250"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 13578.682880424883,
            "unit": "iter/sec",
            "range": "stddev: 0.00016689318054312897",
            "extra": "mean: 73.64484529214586 usec\nrounds: 2831"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 7737.682837161704,
            "unit": "iter/sec",
            "range": "stddev: 0.0009021372469333154",
            "extra": "mean: 129.23765693746304 usec\nrounds: 3816"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 8368.522064463432,
            "unit": "iter/sec",
            "range": "stddev: 0.0006447955616009217",
            "extra": "mean: 119.49541296502721 usec\nrounds: 3056"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 7209.564067410721,
            "unit": "iter/sec",
            "range": "stddev: 0.0007162610634605669",
            "extra": "mean: 138.70464159133897 usec\nrounds: 3560"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 10550.712130697379,
            "unit": "iter/sec",
            "range": "stddev: 0.0007111729292445197",
            "extra": "mean: 94.78033213421605 usec\nrounds: 4161"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 8127.7938203928,
            "unit": "iter/sec",
            "range": "stddev: 0.0007159561168386318",
            "extra": "mean: 123.03461703112836 usec\nrounds: 3580"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 6501.043242220039,
            "unit": "iter/sec",
            "range": "stddev: 0.0008982586890397924",
            "extra": "mean: 153.82146568502293 usec\nrounds: 2978"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 13691.294388213058,
            "unit": "iter/sec",
            "range": "stddev: 0.0015102655161238073",
            "extra": "mean: 73.03911315068265 usec\nrounds: 4154"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 11841.613934825878,
            "unit": "iter/sec",
            "range": "stddev: 0.001265060022485241",
            "extra": "mean: 84.44794818542648 usec\nrounds: 2721"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 13409.840987686848,
            "unit": "iter/sec",
            "range": "stddev: 0.0003694919403579132",
            "extra": "mean: 74.57209976749296 usec\nrounds: 788"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 16277.046644975528,
            "unit": "iter/sec",
            "range": "stddev: 0.0005653142893981593",
            "extra": "mean: 61.43620656814204 usec\nrounds: 4251"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 13385.795879854199,
            "unit": "iter/sec",
            "range": "stddev: 0.0007236224730452871",
            "extra": "mean: 74.70605475950917 usec\nrounds: 3790"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 12950.152187648962,
            "unit": "iter/sec",
            "range": "stddev: 0.0013504553411561866",
            "extra": "mean: 77.21916974487272 usec\nrounds: 2028"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 22247.33449537606,
            "unit": "iter/sec",
            "range": "stddev: 0.0004794620543159024",
            "extra": "mean: 44.9492050478156 usec\nrounds: 4444"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 19142.768197287158,
            "unit": "iter/sec",
            "range": "stddev: 0.0007822116851480485",
            "extra": "mean: 52.23904869420694 usec\nrounds: 3849"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 16693.870361238332,
            "unit": "iter/sec",
            "range": "stddev: 0.0009250432002796389",
            "extra": "mean: 59.90222628791405 usec\nrounds: 3247"
          }
        ]
      }
    ]
  }
}