window.BENCHMARK_DATA = {
  "lastUpdate": 1723715811209,
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
        "date": 1721917653009,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 19031.069548799136,
            "unit": "iter/sec",
            "range": "stddev: 0.0003245554640480211",
            "extra": "mean: 52.54565422273391 usec\nrounds: 2860"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 6658.265963007274,
            "unit": "iter/sec",
            "range": "stddev: 0.0006860892408248649",
            "extra": "mean: 150.189254312746 usec\nrounds: 1736"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 8425.276388974671,
            "unit": "iter/sec",
            "range": "stddev: 0.00118683837364019",
            "extra": "mean: 118.69046828049478 usec\nrounds: 1751"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 14567.93918311165,
            "unit": "iter/sec",
            "range": "stddev: 0.0006375016518406056",
            "extra": "mean: 68.64388898323259 usec\nrounds: 2393"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 12312.080292239192,
            "unit": "iter/sec",
            "range": "stddev: 0.0010000188509723916",
            "extra": "mean: 81.22104276970488 usec\nrounds: 4028"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 8845.145896478765,
            "unit": "iter/sec",
            "range": "stddev: 0.00018265086198521207",
            "extra": "mean: 113.05636014416652 usec\nrounds: 2309"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 11875.18214571955,
            "unit": "iter/sec",
            "range": "stddev: 0.0008377007537219083",
            "extra": "mean: 84.209234665125 usec\nrounds: 3974"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 9677.049012142941,
            "unit": "iter/sec",
            "range": "stddev: 0.0006793421932513292",
            "extra": "mean: 103.3372879216775 usec\nrounds: 3657"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 7936.555924800263,
            "unit": "iter/sec",
            "range": "stddev: 0.0006348271582672414",
            "extra": "mean: 125.99923814247762 usec\nrounds: 3444"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 8936.566969837293,
            "unit": "iter/sec",
            "range": "stddev: 0.0006177748824071234",
            "extra": "mean: 111.89979366519611 usec\nrounds: 3364"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 11803.806585122904,
            "unit": "iter/sec",
            "range": "stddev: 0.0005901364975879342",
            "extra": "mean: 84.71843322647833 usec\nrounds: 3943"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 6823.9767200803035,
            "unit": "iter/sec",
            "range": "stddev: 0.0015935483436176122",
            "extra": "mean: 146.54211774453887 usec\nrounds: 2563"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 7206.379374165662,
            "unit": "iter/sec",
            "range": "stddev: 0.0007898704083594057",
            "extra": "mean: 138.76593891031138 usec\nrounds: 2786"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 22505.13995468248,
            "unit": "iter/sec",
            "range": "stddev: 0.000034025560210271984",
            "extra": "mean: 44.43429376638635 usec\nrounds: 1790"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 7987.503328726624,
            "unit": "iter/sec",
            "range": "stddev: 0.0023537152083207154",
            "extra": "mean: 125.19556597911566 usec\nrounds: 1711"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 12595.718933429853,
            "unit": "iter/sec",
            "range": "stddev: 0.0006439920680174022",
            "extra": "mean: 79.39205418008616 usec\nrounds: 3417"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 11968.006932718738,
            "unit": "iter/sec",
            "range": "stddev: 0.0008146552471261491",
            "extra": "mean: 83.55610133097014 usec\nrounds: 4142"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 12511.401016520082,
            "unit": "iter/sec",
            "range": "stddev: 0.0010186012907225403",
            "extra": "mean: 79.92709998501348 usec\nrounds: 4082"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 14595.441629173922,
            "unit": "iter/sec",
            "range": "stddev: 0.0012394825350714783",
            "extra": "mean: 68.51454210204658 usec\nrounds: 3846"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 19692.83772412713,
            "unit": "iter/sec",
            "range": "stddev: 0.0007137336536914187",
            "extra": "mean: 50.779883224997434 usec\nrounds: 4064"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 19263.282104994312,
            "unit": "iter/sec",
            "range": "stddev: 0.0006505315316849991",
            "extra": "mean: 51.9122335721146 usec\nrounds: 4015"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 22910.75521407579,
            "unit": "iter/sec",
            "range": "stddev: 0.000057178067350342954",
            "extra": "mean: 43.64762272810742 usec\nrounds: 2951"
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
        "date": 1722258594601,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 22236.91941606165,
            "unit": "iter/sec",
            "range": "stddev: 0.00022534930175174982",
            "extra": "mean: 44.97025785314954 usec\nrounds: 1013"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 8508.599138652298,
            "unit": "iter/sec",
            "range": "stddev: 0.0005864920635074544",
            "extra": "mean: 117.52815988912518 usec\nrounds: 2076"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 10785.715073556143,
            "unit": "iter/sec",
            "range": "stddev: 0.0007947802046331334",
            "extra": "mean: 92.71522501570139 usec\nrounds: 3937"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 15177.803645087153,
            "unit": "iter/sec",
            "range": "stddev: 0.0008740125863207516",
            "extra": "mean: 65.88568566201516 usec\nrounds: 2307"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 20237.23818787714,
            "unit": "iter/sec",
            "range": "stddev: 0.0004467349755641742",
            "extra": "mean: 49.413857301884065 usec\nrounds: 9715"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 9907.626694807435,
            "unit": "iter/sec",
            "range": "stddev: 0.000847610375127883",
            "extra": "mean: 100.93234543486562 usec\nrounds: 5670"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 15765.866547498952,
            "unit": "iter/sec",
            "range": "stddev: 0.0005704667799210182",
            "extra": "mean: 63.42816596773977 usec\nrounds: 11160"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 11181.680250914183,
            "unit": "iter/sec",
            "range": "stddev: 0.0009402586268458702",
            "extra": "mean: 89.43199747803938 usec\nrounds: 4790"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 10560.767201881948,
            "unit": "iter/sec",
            "range": "stddev: 0.00015329679290521583",
            "extra": "mean: 94.69009030156427 usec\nrounds: 3562"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 11243.539949970671,
            "unit": "iter/sec",
            "range": "stddev: 0.000600926318463414",
            "extra": "mean: 88.93996058622164 usec\nrounds: 7337"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 13111.1215391941,
            "unit": "iter/sec",
            "range": "stddev: 0.0008766118793970339",
            "extra": "mean: 76.27112577750285 usec\nrounds: 9283"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 8647.058005092997,
            "unit": "iter/sec",
            "range": "stddev: 0.00023458649478922148",
            "extra": "mean: 115.64626944921775 usec\nrounds: 4105"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 7283.812288759804,
            "unit": "iter/sec",
            "range": "stddev: 0.00251910352408195",
            "extra": "mean: 137.29074286320844 usec\nrounds: 3120"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 20305.042088713213,
            "unit": "iter/sec",
            "range": "stddev: 0.0009975046002292992",
            "extra": "mean: 49.248851375484776 usec\nrounds: 2922"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 31091.170736719083,
            "unit": "iter/sec",
            "range": "stddev: 0.00006650986748731508",
            "extra": "mean: 32.163472018086054 usec\nrounds: 2796"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 18426.401615373987,
            "unit": "iter/sec",
            "range": "stddev: 0.0010315968540002406",
            "extra": "mean: 54.269955733823494 usec\nrounds: 2178"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 24478.82752811921,
            "unit": "iter/sec",
            "range": "stddev: 0.00015604809539241748",
            "extra": "mean: 40.85162979522954 usec\nrounds: 4370"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 17297.45426951285,
            "unit": "iter/sec",
            "range": "stddev: 0.001100330815385297",
            "extra": "mean: 57.81197535885511 usec\nrounds: 4197"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 21168.917699073478,
            "unit": "iter/sec",
            "range": "stddev: 0.0008431612469312656",
            "extra": "mean: 47.23907070807725 usec\nrounds: 3863"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37670.201005605566,
            "unit": "iter/sec",
            "range": "stddev: 0.000045231473082822714",
            "extra": "mean: 26.546181684859967 usec\nrounds: 1963"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 35313.207077725645,
            "unit": "iter/sec",
            "range": "stddev: 0.00005731088279801849",
            "extra": "mean: 28.31801704668069 usec\nrounds: 1795"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 34456.4794188783,
            "unit": "iter/sec",
            "range": "stddev: 0.00006605682909775632",
            "extra": "mean: 29.02211766452587 usec\nrounds: 2228"
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
        "date": 1722273645971,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 13156.33271911668,
            "unit": "iter/sec",
            "range": "stddev: 0.0001578580796349302",
            "extra": "mean: 76.00902328556649 usec\nrounds: 2095"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4911.234247932994,
            "unit": "iter/sec",
            "range": "stddev: 0.0011736370198682563",
            "extra": "mean: 203.6148042461776 usec\nrounds: 1257"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 13455.251039434279,
            "unit": "iter/sec",
            "range": "stddev: 0.0006052285159020938",
            "extra": "mean: 74.32042680357488 usec\nrounds: 3849"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 17606.458000073184,
            "unit": "iter/sec",
            "range": "stddev: 0.0007572739846879481",
            "extra": "mean: 56.797341066320286 usec\nrounds: 3177"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 16016.759738038878,
            "unit": "iter/sec",
            "range": "stddev: 0.0004597693936267773",
            "extra": "mean: 62.43460077790004 usec\nrounds: 9302"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 9286.89164603652,
            "unit": "iter/sec",
            "range": "stddev: 0.0008751226379219172",
            "extra": "mean: 107.67865483030398 usec\nrounds: 3801"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 11848.699852195712,
            "unit": "iter/sec",
            "range": "stddev: 0.000889089507368525",
            "extra": "mean: 84.3974454981816 usec\nrounds: 6072"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 9466.002087998339,
            "unit": "iter/sec",
            "range": "stddev: 0.0007926317477901668",
            "extra": "mean: 105.6412190388031 usec\nrounds: 6559"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 8705.859341103938,
            "unit": "iter/sec",
            "range": "stddev: 0.0009054928044000427",
            "extra": "mean: 114.86516848240232 usec\nrounds: 5525"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 10851.07446294806,
            "unit": "iter/sec",
            "range": "stddev: 0.0006275753758517239",
            "extra": "mean: 92.15677243894946 usec\nrounds: 7324"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 16206.681945244105,
            "unit": "iter/sec",
            "range": "stddev: 0.0005072288146593734",
            "extra": "mean: 61.702944710002946 usec\nrounds: 8349"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 11985.55180294181,
            "unit": "iter/sec",
            "range": "stddev: 0.0006515993357432802",
            "extra": "mean: 83.43378898538101 usec\nrounds: 6252"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 9820.397855951102,
            "unit": "iter/sec",
            "range": "stddev: 0.0011200059410414966",
            "extra": "mean: 101.82886830740834 usec\nrounds: 3201"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 25520.30884736055,
            "unit": "iter/sec",
            "range": "stddev: 0.0006514391862229044",
            "extra": "mean: 39.18447876086051 usec\nrounds: 4709"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 33717.98607775599,
            "unit": "iter/sec",
            "range": "stddev: 0.00010052417300014325",
            "extra": "mean: 29.65776181572445 usec\nrounds: 4698"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 23010.699122464863,
            "unit": "iter/sec",
            "range": "stddev: 0.0008812262379002267",
            "extra": "mean: 43.45804508928288 usec\nrounds: 3291"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 26264.795369411906,
            "unit": "iter/sec",
            "range": "stddev: 0.0005887017329766615",
            "extra": "mean: 38.07377845268135 usec\nrounds: 4554"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 34094.86679900115,
            "unit": "iter/sec",
            "range": "stddev: 0.000033059565318103144",
            "extra": "mean: 29.329928340687815 usec\nrounds: 4746"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 17772.839102662027,
            "unit": "iter/sec",
            "range": "stddev: 0.0009011710905480738",
            "extra": "mean: 56.26563061892681 usec\nrounds: 4286"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 17206.834437615853,
            "unit": "iter/sec",
            "range": "stddev: 0.000662288562416348",
            "extra": "mean: 58.11644225586901 usec\nrounds: 4743"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 31738.018573292287,
            "unit": "iter/sec",
            "range": "stddev: 0.00006731901644163052",
            "extra": "mean: 31.50795307812648 usec\nrounds: 2554"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 18265.272512183757,
            "unit": "iter/sec",
            "range": "stddev: 0.0010461813998308889",
            "extra": "mean: 54.74870409587128 usec\nrounds: 3167"
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
        "date": 1722450142041,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 16312.690283750546,
            "unit": "iter/sec",
            "range": "stddev: 0.00010371049437739866",
            "extra": "mean: 61.301966910762935 usec\nrounds: 2090"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4957.862738714556,
            "unit": "iter/sec",
            "range": "stddev: 0.0008269833270967935",
            "extra": "mean: 201.6998155659456 usec\nrounds: 1884"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 7002.589094344397,
            "unit": "iter/sec",
            "range": "stddev: 0.0016705855498097418",
            "extra": "mean: 142.80432373329523 usec\nrounds: 1853"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 16891.679856036495,
            "unit": "iter/sec",
            "range": "stddev: 0.00026759675614745665",
            "extra": "mean: 59.200743118668264 usec\nrounds: 3799"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 16825.351470175792,
            "unit": "iter/sec",
            "range": "stddev: 0.0009739795903540419",
            "extra": "mean: 59.4341224771783 usec\nrounds: 7021"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 11799.992201946043,
            "unit": "iter/sec",
            "range": "stddev: 0.0007054758051874686",
            "extra": "mean: 84.74581871631077 usec\nrounds: 6823"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 22523.930204059903,
            "unit": "iter/sec",
            "range": "stddev: 0.000046547843769971536",
            "extra": "mean: 44.39722512635702 usec\nrounds: 3459"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 9335.86507037998,
            "unit": "iter/sec",
            "range": "stddev: 0.0014100309123570153",
            "extra": "mean: 107.11380171642723 usec\nrounds: 2172"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 7500.929521821653,
            "unit": "iter/sec",
            "range": "stddev: 0.0005727920931782544",
            "extra": "mean: 133.31681054872024 usec\nrounds: 6683"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 7791.410585504101,
            "unit": "iter/sec",
            "range": "stddev: 0.001229983270587126",
            "extra": "mean: 128.34646422824866 usec\nrounds: 6423"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 15147.282265047097,
            "unit": "iter/sec",
            "range": "stddev: 0.000490531552072565",
            "extra": "mean: 66.01844360605442 usec\nrounds: 9854"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 11256.23971891377,
            "unit": "iter/sec",
            "range": "stddev: 0.0006731789787844687",
            "extra": "mean: 88.83961473561264 usec\nrounds: 6595"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 6273.211818089874,
            "unit": "iter/sec",
            "range": "stddev: 0.0017713515182943092",
            "extra": "mean: 159.4079761688151 usec\nrounds: 1713"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 26635.58894083825,
            "unit": "iter/sec",
            "range": "stddev: 0.0005446794070837394",
            "extra": "mean: 37.54375404355256 usec\nrounds: 5031"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 43495.67037975332,
            "unit": "iter/sec",
            "range": "stddev: 0.000041463276962439785",
            "extra": "mean: 22.9907940553432 usec\nrounds: 4279"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 22564.254605576072,
            "unit": "iter/sec",
            "range": "stddev: 0.0008844129157717473",
            "extra": "mean: 44.3178831953474 usec\nrounds: 4580"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 25065.77771117995,
            "unit": "iter/sec",
            "range": "stddev: 0.000930583830965818",
            "extra": "mean: 39.89503184471214 usec\nrounds: 4421"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 26523.85707864414,
            "unit": "iter/sec",
            "range": "stddev: 0.00017340276207232884",
            "extra": "mean: 37.70190726917906 usec\nrounds: 3900"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 21312.11104197007,
            "unit": "iter/sec",
            "range": "stddev: 0.0007659671983499741",
            "extra": "mean: 46.9216774457816 usec\nrounds: 4365"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 21354.056647515295,
            "unit": "iter/sec",
            "range": "stddev: 0.00005568748351770502",
            "extra": "mean: 46.829509563765136 usec\nrounds: 2122"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 10766.37975136164,
            "unit": "iter/sec",
            "range": "stddev: 0.0010745408363957126",
            "extra": "mean: 92.88173212295698 usec\nrounds: 3219"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 16068.934408308276,
            "unit": "iter/sec",
            "range": "stddev: 0.00022866663987600332",
            "extra": "mean: 62.23188013531006 usec\nrounds: 3980"
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
        "date": 1722513361400,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 8716.708217132928,
            "unit": "iter/sec",
            "range": "stddev: 0.00004933688374961259",
            "extra": "mean: 114.72220649011433 usec\nrounds: 8"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4885.30260381316,
            "unit": "iter/sec",
            "range": "stddev: 0.0006263572999197418",
            "extra": "mean: 204.69561071190614 usec\nrounds: 1510"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 6635.956555935106,
            "unit": "iter/sec",
            "range": "stddev: 0.0011882152736285832",
            "extra": "mean: 150.6941752211464 usec\nrounds: 3031"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 11436.177019054934,
            "unit": "iter/sec",
            "range": "stddev: 0.00017154299168851603",
            "extra": "mean: 87.44180842372431 usec\nrounds: 2058"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 13424.074325867348,
            "unit": "iter/sec",
            "range": "stddev: 0.0005642993369165428",
            "extra": "mean: 74.49303212461083 usec\nrounds: 5806"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 8654.668516473226,
            "unit": "iter/sec",
            "range": "stddev: 0.0009604980938295448",
            "extra": "mean: 115.54457551974498 usec\nrounds: 3634"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 16452.01087693325,
            "unit": "iter/sec",
            "range": "stddev: 0.0004594164515302232",
            "extra": "mean: 60.78284335455081 usec\nrounds: 12415"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 8055.399269303103,
            "unit": "iter/sec",
            "range": "stddev: 0.0014624835989039972",
            "extra": "mean: 124.140339487668 usec\nrounds: 4311"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 6844.053618084486,
            "unit": "iter/sec",
            "range": "stddev: 0.0010319982106626914",
            "extra": "mean: 146.11223929596858 usec\nrounds: 5188"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 8492.239356841748,
            "unit": "iter/sec",
            "range": "stddev: 0.001228055072566545",
            "extra": "mean: 117.75457072984558 usec\nrounds: 6647"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 11781.932468739891,
            "unit": "iter/sec",
            "range": "stddev: 0.0013230225175649645",
            "extra": "mean: 84.8757198917261 usec\nrounds: 5175"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 7783.614908273641,
            "unit": "iter/sec",
            "range": "stddev: 0.00041966430000421406",
            "extra": "mean: 128.47500959188562 usec\nrounds: 3103"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 6446.435051285292,
            "unit": "iter/sec",
            "range": "stddev: 0.0013583242840668533",
            "extra": "mean: 155.12449781071166 usec\nrounds: 1639"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 27014.170763028662,
            "unit": "iter/sec",
            "range": "stddev: 0.0005944618649034061",
            "extra": "mean: 37.017608601504456 usec\nrounds: 4487"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 24911.34393624782,
            "unit": "iter/sec",
            "range": "stddev: 0.00018582847319422523",
            "extra": "mean: 40.14235452567965 usec\nrounds: 4696"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 12731.07740218625,
            "unit": "iter/sec",
            "range": "stddev: 0.0017073929818126536",
            "extra": "mean: 78.54794754670759 usec\nrounds: 1782"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 35480.8492368142,
            "unit": "iter/sec",
            "range": "stddev: 0.000054713283033644864",
            "extra": "mean: 28.18421828986045 usec\nrounds: 1937"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 23702.837349652473,
            "unit": "iter/sec",
            "range": "stddev: 0.0008711115453770025",
            "extra": "mean: 42.189041980438766 usec\nrounds: 4545"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 32276.833271510277,
            "unit": "iter/sec",
            "range": "stddev: 0.00004096138120210762",
            "extra": "mean: 30.981973714337947 usec\nrounds: 2740"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 21053.434021287663,
            "unit": "iter/sec",
            "range": "stddev: 0.00004786682662123441",
            "extra": "mean: 47.49818955847652 usec\nrounds: 2963"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 12229.15952288202,
            "unit": "iter/sec",
            "range": "stddev: 0.0015420975854940372",
            "extra": "mean: 81.77176838104832 usec\nrounds: 3313"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 18584.36179513787,
            "unit": "iter/sec",
            "range": "stddev: 0.000056598974963303534",
            "extra": "mean: 53.80868124627368 usec\nrounds: 3016"
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
        "date": 1722527093439,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 7349.163131845333,
            "unit": "iter/sec",
            "range": "stddev: 0.00012349964733862628",
            "extra": "mean: 136.0699146365126 usec\nrounds: 6"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4004.216940879329,
            "unit": "iter/sec",
            "range": "stddev: 0.0009719883973007312",
            "extra": "mean: 249.7367187554027 usec\nrounds: 1790"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 8571.968930904659,
            "unit": "iter/sec",
            "range": "stddev: 0.0008938626358969132",
            "extra": "mean: 116.65931223743517 usec\nrounds: 2747"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 17338.649556406588,
            "unit": "iter/sec",
            "range": "stddev: 0.00008035807685600609",
            "extra": "mean: 57.67461858818771 usec\nrounds: 3408"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 12087.808239899885,
            "unit": "iter/sec",
            "range": "stddev: 0.0012461657034107212",
            "extra": "mean: 82.72798344857614 usec\nrounds: 8662"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 8886.485888651221,
            "unit": "iter/sec",
            "range": "stddev: 0.0007046581640579106",
            "extra": "mean: 112.53042119574881 usec\nrounds: 6522"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 17369.952199366868,
            "unit": "iter/sec",
            "range": "stddev: 0.0001782987638466997",
            "extra": "mean: 57.570682320959406 usec\nrounds: 5218"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 10203.288906367125,
            "unit": "iter/sec",
            "range": "stddev: 0.0011661370276906157",
            "extra": "mean: 98.00761393475523 usec\nrounds: 6045"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 9851.175146377736,
            "unit": "iter/sec",
            "range": "stddev: 0.000111049333979768",
            "extra": "mean: 101.51073198284355 usec\nrounds: 5528"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 8410.691634358554,
            "unit": "iter/sec",
            "range": "stddev: 0.0014574216322853482",
            "extra": "mean: 118.89628623583054 usec\nrounds: 5587"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 12572.221875195704,
            "unit": "iter/sec",
            "range": "stddev: 0.0007673254980375275",
            "extra": "mean: 79.54043524899481 usec\nrounds: 8766"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 8400.879781844606,
            "unit": "iter/sec",
            "range": "stddev: 0.0008225257073847136",
            "extra": "mean: 119.0351517898316 usec\nrounds: 6142"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 11425.825901795677,
            "unit": "iter/sec",
            "range": "stddev: 0.00007467299930582255",
            "extra": "mean: 87.52102549040595 usec\nrounds: 2024"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 25153.171008794645,
            "unit": "iter/sec",
            "range": "stddev: 0.000938885749244293",
            "extra": "mean: 39.75641876924211 usec\nrounds: 4886"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 24599.120708116247,
            "unit": "iter/sec",
            "range": "stddev: 0.0006392185833933539",
            "extra": "mean: 40.65185954675442 usec\nrounds: 5031"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 33692.327806139125,
            "unit": "iter/sec",
            "range": "stddev: 0.00004465315117178024",
            "extra": "mean: 29.68034757805569 usec\nrounds: 4657"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 20703.130426321768,
            "unit": "iter/sec",
            "range": "stddev: 0.0011999436317408063",
            "extra": "mean: 48.30187413245531 usec\nrounds: 3238"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 21304.872119418447,
            "unit": "iter/sec",
            "range": "stddev: 0.0006841682781482323",
            "extra": "mean: 46.937620390058306 usec\nrounds: 4020"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 33332.90452584623,
            "unit": "iter/sec",
            "range": "stddev: 0.00003894505440527275",
            "extra": "mean: 30.000385931703104 usec\nrounds: 2216"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 13792.0808305384,
            "unit": "iter/sec",
            "range": "stddev: 0.00018344842288293498",
            "extra": "mean: 72.50537553302341 usec\nrounds: 3138"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 11093.314086595161,
            "unit": "iter/sec",
            "range": "stddev: 0.00137347391632102",
            "extra": "mean: 90.14438716815664 usec\nrounds: 3850"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 13832.544037718098,
            "unit": "iter/sec",
            "range": "stddev: 0.00026716561630298215",
            "extra": "mean: 72.29328150145301 usec\nrounds: 2427"
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
        "date": 1722583632915,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 23640.959054134262,
            "unit": "iter/sec",
            "range": "stddev: 0.000015028212191167697",
            "extra": "mean: 42.29946838070949 usec\nrounds: 6"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 4870.41065472,
            "unit": "iter/sec",
            "range": "stddev: 0.0009049564970810484",
            "extra": "mean: 205.32149563833647 usec\nrounds: 1377"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 11710.46382376243,
            "unit": "iter/sec",
            "range": "stddev: 0.00016760556638437793",
            "extra": "mean: 85.39371412179574 usec\nrounds: 1208"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 16198.385979217623,
            "unit": "iter/sec",
            "range": "stddev: 0.0009002266622559695",
            "extra": "mean: 61.73454573085187 usec\nrounds: 3709"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 19053.214177430553,
            "unit": "iter/sec",
            "range": "stddev: 0.00045332656379552084",
            "extra": "mean: 52.48458295212721 usec\nrounds: 7865"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 8864.509700761271,
            "unit": "iter/sec",
            "range": "stddev: 0.0008728607715098405",
            "extra": "mean: 112.80939767194586 usec\nrounds: 6034"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 17085.624855152993,
            "unit": "iter/sec",
            "range": "stddev: 0.0006406751855374878",
            "extra": "mean: 58.52873444651348 usec\nrounds: 9258"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 9198.90738236188,
            "unit": "iter/sec",
            "range": "stddev: 0.0010767443401426692",
            "extra": "mean: 108.7085627057638 usec\nrounds: 3118"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 7014.142962865743,
            "unit": "iter/sec",
            "range": "stddev: 0.0007028423358281084",
            "extra": "mean: 142.56909294466868 usec\nrounds: 4939"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 7962.397897763129,
            "unit": "iter/sec",
            "range": "stddev: 0.00036642155022740793",
            "extra": "mean: 125.59030744757548 usec\nrounds: 4381"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 10512.849703969227,
            "unit": "iter/sec",
            "range": "stddev: 0.0016755746202692609",
            "extra": "mean: 95.12168709331405 usec\nrounds: 2741"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 7735.729869076081,
            "unit": "iter/sec",
            "range": "stddev: 0.00030652009278732786",
            "extra": "mean: 129.2702843719432 usec\nrounds: 1569"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 7946.58189390683,
            "unit": "iter/sec",
            "range": "stddev: 0.0003919265952226601",
            "extra": "mean: 125.84026860237434 usec\nrounds: 1724"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 41081.19292947642,
            "unit": "iter/sec",
            "range": "stddev: 0.000036749709140225453",
            "extra": "mean: 24.342038988903944 usec\nrounds: 2923"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 28885.785332291358,
            "unit": "iter/sec",
            "range": "stddev: 0.0005773776543238641",
            "extra": "mean: 34.61910377358174 usec\nrounds: 5069"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 39417.62270685119,
            "unit": "iter/sec",
            "range": "stddev: 0.000033197024517551246",
            "extra": "mean: 25.369363531560463 usec\nrounds: 4297"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 24330.49564032545,
            "unit": "iter/sec",
            "range": "stddev: 0.0012067953112953412",
            "extra": "mean: 41.10068347077141 usec\nrounds: 4740"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 24338.584261913555,
            "unit": "iter/sec",
            "range": "stddev: 0.0007379480045519077",
            "extra": "mean: 41.087024176868766 usec\nrounds: 3279"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 29050.06534568439,
            "unit": "iter/sec",
            "range": "stddev: 0.00012175273829289664",
            "extra": "mean: 34.4233304848162 usec\nrounds: 3827"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 15733.787700874853,
            "unit": "iter/sec",
            "range": "stddev: 0.0008599970739773874",
            "extra": "mean: 63.55748653862899 usec\nrounds: 3502"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 18013.516091699446,
            "unit": "iter/sec",
            "range": "stddev: 0.00008241938045151544",
            "extra": "mean: 55.5138705241891 usec\nrounds: 3731"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 8648.40947151146,
            "unit": "iter/sec",
            "range": "stddev: 0.002324448141653864",
            "extra": "mean: 115.62819768121277 usec\nrounds: 1725"
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
        "date": 1722599693968,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 12934.18853729196,
            "unit": "iter/sec",
            "range": "stddev: 0.000019744492699081047",
            "extra": "mean: 77.31447528515542 usec\nrounds: 7"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 715.5479268162156,
            "unit": "iter/sec",
            "range": "stddev: 0.0005731526950761086",
            "extra": "mean: 1.3975304274158624 msec\nrounds: 655"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 131.11678711022714,
            "unit": "iter/sec",
            "range": "stddev: 0.0029395779613463464",
            "extra": "mean: 7.626788468812318 msec\nrounds: 85"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 13.595300645442853,
            "unit": "iter/sec",
            "range": "stddev: 0.01266921703240999",
            "extra": "mean: 73.55482795705589 msec\nrounds: 13"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 5885.815518667834,
            "unit": "iter/sec",
            "range": "stddev: 0.0006600344910655319",
            "extra": "mean: 169.89999037997964 usec\nrounds: 3080"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 7958.562993452193,
            "unit": "iter/sec",
            "range": "stddev: 0.000949678917548173",
            "extra": "mean: 125.65082425341576 usec\nrounds: 2919"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 15523.592325441168,
            "unit": "iter/sec",
            "range": "stddev: 0.000714173563389617",
            "extra": "mean: 64.41807920716448 usec\nrounds: 3520"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 17117.271261910562,
            "unit": "iter/sec",
            "range": "stddev: 0.00042295343035057115",
            "extra": "mean: 58.4205265371476 usec\nrounds: 10088"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 9544.524049429348,
            "unit": "iter/sec",
            "range": "stddev: 0.0008070529612046622",
            "extra": "mean: 104.77211800412283 usec\nrounds: 5550"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 17464.85870796778,
            "unit": "iter/sec",
            "range": "stddev: 0.0006176985209526498",
            "extra": "mean: 57.257835103113784 usec\nrounds: 12103"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 11681.049153266864,
            "unit": "iter/sec",
            "range": "stddev: 0.0009991021982340403",
            "extra": "mean: 85.60874857035662 usec\nrounds: 6299"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 8486.623164998233,
            "unit": "iter/sec",
            "range": "stddev: 0.0005231287700872981",
            "extra": "mean: 117.83249716145588 usec\nrounds: 6346"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 9465.554986779303,
            "unit": "iter/sec",
            "range": "stddev: 0.0007009379007954607",
            "extra": "mean: 105.64620895412013 usec\nrounds: 3789"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 16310.492883381874,
            "unit": "iter/sec",
            "range": "stddev: 0.0004228846908313876",
            "extra": "mean: 61.31022570255133 usec\nrounds: 7509"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 10266.585361693784,
            "unit": "iter/sec",
            "range": "stddev: 0.0006874706535145892",
            "extra": "mean: 97.40336877060942 usec\nrounds: 4118"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 9526.353991095304,
            "unit": "iter/sec",
            "range": "stddev: 0.0008638685397858229",
            "extra": "mean: 104.97195474099989 usec\nrounds: 3188"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 30219.73396543306,
            "unit": "iter/sec",
            "range": "stddev: 0.0001760187022431684",
            "extra": "mean: 33.09095973987902 usec\nrounds: 4840"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 27719.648505304693,
            "unit": "iter/sec",
            "range": "stddev: 0.00009986456872751466",
            "extra": "mean: 36.07549351892506 usec\nrounds: 1542"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 23973.78161648634,
            "unit": "iter/sec",
            "range": "stddev: 0.0009432270240930434",
            "extra": "mean: 41.71223447335976 usec\nrounds: 4721"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 27163.54440816848,
            "unit": "iter/sec",
            "range": "stddev: 0.0007088456988071282",
            "extra": "mean: 36.81404698052899 usec\nrounds: 3153"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 31640.30887386523,
            "unit": "iter/sec",
            "range": "stddev: 0.00010460475406353095",
            "extra": "mean: 31.605254044343294 usec\nrounds: 4492"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 18651.10276232859,
            "unit": "iter/sec",
            "range": "stddev: 0.0009418190797074387",
            "extra": "mean: 53.61613266212844 usec\nrounds: 4350"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 18055.068382049227,
            "unit": "iter/sec",
            "range": "stddev: 0.00007750467708113758",
            "extra": "mean: 55.38610980804833 usec\nrounds: 611"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 12936.585364775285,
            "unit": "iter/sec",
            "range": "stddev: 0.0012653365323753764",
            "extra": "mean: 77.30015083600622 usec\nrounds: 2725"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 14604.183231752602,
            "unit": "iter/sec",
            "range": "stddev: 0.00014784789217400955",
            "extra": "mean: 68.4735314622585 usec\nrounds: 3507"
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
        "date": 1722859179087,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 8856.344783356086,
            "unit": "iter/sec",
            "range": "stddev: 0.00009348905079660019",
            "extra": "mean: 112.913399880199 usec\nrounds: 5"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 962.1175467043563,
            "unit": "iter/sec",
            "range": "stddev: 0.0004910469543516839",
            "extra": "mean: 1.0393740384690067 msec\nrounds: 754"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 137.60445194752674,
            "unit": "iter/sec",
            "range": "stddev: 0.0021443199228069086",
            "extra": "mean: 7.267206735297591 msec\nrounds: 170"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 13.588668490864642,
            "unit": "iter/sec",
            "range": "stddev: 0.013587485418514943",
            "extra": "mean: 73.59072750006946 msec\nrounds: 14"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 8422.837204208456,
            "unit": "iter/sec",
            "range": "stddev: 0.00045702505012845283",
            "extra": "mean: 118.72484006937138 usec\nrounds: 3189"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 8981.649268785073,
            "unit": "iter/sec",
            "range": "stddev: 0.0011565136362662034",
            "extra": "mean: 111.3381262253706 usec\nrounds: 3874"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 19120.225319734676,
            "unit": "iter/sec",
            "range": "stddev: 0.00006742371580296056",
            "extra": "mean: 52.30063889298751 usec\nrounds: 3589"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 15790.568299944362,
            "unit": "iter/sec",
            "range": "stddev: 0.0007333830941612978",
            "extra": "mean: 63.328943012362856 usec\nrounds: 10002"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 10668.671327218994,
            "unit": "iter/sec",
            "range": "stddev: 0.0007676480495714512",
            "extra": "mean: 93.73238422376916 usec\nrounds: 6543"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 19087.036919080183,
            "unit": "iter/sec",
            "range": "stddev: 0.0001141722006833758",
            "extra": "mean: 52.391578862634205 usec\nrounds: 3538"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 11066.953074743958,
            "unit": "iter/sec",
            "range": "stddev: 0.0007361890238479959",
            "extra": "mean: 90.35910726703209 usec\nrounds: 6992"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 7879.618286161504,
            "unit": "iter/sec",
            "range": "stddev: 0.0008063222210754015",
            "extra": "mean: 126.90970091231948 usec\nrounds: 5256"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 9968.695197232384,
            "unit": "iter/sec",
            "range": "stddev: 0.0005088781654827072",
            "extra": "mean: 100.31403109582794 usec\nrounds: 7268"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 15565.071795245316,
            "unit": "iter/sec",
            "range": "stddev: 0.0005763516728231208",
            "extra": "mean: 64.24641101273117 usec\nrounds: 9316"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 10378.669025139608,
            "unit": "iter/sec",
            "range": "stddev: 0.0009122519354425193",
            "extra": "mean: 96.35146834124508 usec\nrounds: 4501"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 10717.178280737535,
            "unit": "iter/sec",
            "range": "stddev: 0.00010752428809965803",
            "extra": "mean: 93.3081426663719 usec\nrounds: 2222"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 23110.414645628312,
            "unit": "iter/sec",
            "range": "stddev: 0.000820990525075868",
            "extra": "mean: 43.270534749542676 usec\nrounds: 4763"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 27306.299873117965,
            "unit": "iter/sec",
            "range": "stddev: 0.0002079873092873096",
            "extra": "mean: 36.62158566508906 usec\nrounds: 2720"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 11552.860432183554,
            "unit": "iter/sec",
            "range": "stddev: 0.0017429330914947713",
            "extra": "mean: 86.55864977077321 usec\nrounds: 1125"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 38333.98644139083,
            "unit": "iter/sec",
            "range": "stddev: 0.00007805128182307904",
            "extra": "mean: 26.086512070141957 usec\nrounds: 4474"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 29252.809412682283,
            "unit": "iter/sec",
            "range": "stddev: 0.0006094440159212587",
            "extra": "mean: 34.18475080094219 usec\nrounds: 4025"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 24290.751800296865,
            "unit": "iter/sec",
            "range": "stddev: 0.0006946425691246746",
            "extra": "mean: 41.1679312448361 usec\nrounds: 4523"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 22254.979044898642,
            "unit": "iter/sec",
            "range": "stddev: 0.00002704667535158535",
            "extra": "mean: 44.93376506814654 usec\nrounds: 3052"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 16260.863126016757,
            "unit": "iter/sec",
            "range": "stddev: 0.0007827482784901873",
            "extra": "mean: 61.497350555767134 usec\nrounds: 3523"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 21257.740110577262,
            "unit": "iter/sec",
            "range": "stddev: 0.000037752564826716235",
            "extra": "mean: 47.04168904118024 usec\nrounds: 3978"
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
        "date": 1722868457067,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 40024.85758247588,
            "unit": "iter/sec",
            "range": "stddev: 0.00000920532500168212",
            "extra": "mean: 24.98447365963473 usec\nrounds: 19"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2326.436144154428,
            "unit": "iter/sec",
            "range": "stddev: 0.0001470481825260836",
            "extra": "mean: 429.8420150119626 usec\nrounds: 1932"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 291.34856027428634,
            "unit": "iter/sec",
            "range": "stddev: 0.00013793626185681262",
            "extra": "mean: 3.432314884475704 msec\nrounds: 277"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 29.14573321279987,
            "unit": "iter/sec",
            "range": "stddev: 0.0004663688490120993",
            "extra": "mean: 34.3103394482741 msec\nrounds: 29"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14070.779967302216,
            "unit": "iter/sec",
            "range": "stddev: 0.00033087208207893605",
            "extra": "mean: 71.06926569271977 usec\nrounds: 5002"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20872.771754993348,
            "unit": "iter/sec",
            "range": "stddev: 0.0005096663042607896",
            "extra": "mean: 47.909305565072934 usec\nrounds: 5714"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 35235.56428052978,
            "unit": "iter/sec",
            "range": "stddev: 0.0003973257192788941",
            "extra": "mean: 28.38041678681368 usec\nrounds: 5528"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 39369.77940070521,
            "unit": "iter/sec",
            "range": "stddev: 0.0002765767420533634",
            "extra": "mean: 25.40019312330939 usec\nrounds: 10615"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21447.950296519302,
            "unit": "iter/sec",
            "range": "stddev: 0.00033538253441162016",
            "extra": "mean: 46.624501930251384 usec\nrounds: 9848"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 36467.85949268325,
            "unit": "iter/sec",
            "range": "stddev: 0.0003450588606235144",
            "extra": "mean: 27.42140651826948 usec\nrounds: 9542"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23606.95272241237,
            "unit": "iter/sec",
            "range": "stddev: 0.0003352843683627917",
            "extra": "mean: 42.3604016900751 usec\nrounds: 9826"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 17545.54961475477,
            "unit": "iter/sec",
            "range": "stddev: 0.0003669772658669031",
            "extra": "mean: 56.99450983051902 usec\nrounds: 8699"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20803.154802722755,
            "unit": "iter/sec",
            "range": "stddev: 0.0003195751180890634",
            "extra": "mean: 48.0696322016081 usec\nrounds: 9391"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 32220.318123687004,
            "unit": "iter/sec",
            "range": "stddev: 0.0003118920945890012",
            "extra": "mean: 31.036316778785704 usec\nrounds: 11033"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20245.05275889894,
            "unit": "iter/sec",
            "range": "stddev: 0.0003836774841847903",
            "extra": "mean: 49.394783600178016 usec\nrounds: 10000"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20946.552885831432,
            "unit": "iter/sec",
            "range": "stddev: 0.0004776478595649237",
            "extra": "mean: 47.74055213048516 usec\nrounds: 5160"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 54625.21759224672,
            "unit": "iter/sec",
            "range": "stddev: 0.0003827917205941667",
            "extra": "mean: 18.306563233570273 usec\nrounds: 8508"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 64977.83177560553,
            "unit": "iter/sec",
            "range": "stddev: 0.0003060298209124033",
            "extra": "mean: 15.389864091701309 usec\nrounds: 8962"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 58224.01032447901,
            "unit": "iter/sec",
            "range": "stddev: 0.00034845742186845644",
            "extra": "mean: 17.175045044596867 usec\nrounds: 8103"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 61884.321596623035,
            "unit": "iter/sec",
            "range": "stddev: 0.00030586153265851874",
            "extra": "mean: 16.159181747490774 usec\nrounds: 7901"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 57882.05880507956,
            "unit": "iter/sec",
            "range": "stddev: 0.00028431908762723126",
            "extra": "mean: 17.276510556881625 usec\nrounds: 7010"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 57476.17175966343,
            "unit": "iter/sec",
            "range": "stddev: 0.00027731492504104536",
            "extra": "mean: 17.39851436490063 usec\nrounds: 7415"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 35519.99555146268,
            "unit": "iter/sec",
            "range": "stddev: 0.00034536655485204815",
            "extra": "mean: 28.15315667906442 usec\nrounds: 5323"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 34142.925128135204,
            "unit": "iter/sec",
            "range": "stddev: 0.0003201052356560613",
            "extra": "mean: 29.2886446093032 usec\nrounds: 5546"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 36016.21207816669,
            "unit": "iter/sec",
            "range": "stddev: 0.00032611080715446995",
            "extra": "mean: 27.765274089059684 usec\nrounds: 6279"
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
        "date": 1722950387549,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 48837.18658500567,
            "unit": "iter/sec",
            "range": "stddev: 0.00000776915004509518",
            "extra": "mean: 20.476200000985045 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2486.732784632959,
            "unit": "iter/sec",
            "range": "stddev: 0.0001482034327455714",
            "extra": "mean: 402.134079777132 usec\nrounds: 2156"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 320.79408134208575,
            "unit": "iter/sec",
            "range": "stddev: 0.00010589632970536238",
            "extra": "mean: 3.1172644950815918 msec\nrounds: 305"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 30.85237313865189,
            "unit": "iter/sec",
            "range": "stddev: 0.0006770140666400489",
            "extra": "mean: 32.41241753125301 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15179.868547681757,
            "unit": "iter/sec",
            "range": "stddev: 0.0003653648365941007",
            "extra": "mean: 65.87672329696942 usec\nrounds: 4962"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20684.453077578542,
            "unit": "iter/sec",
            "range": "stddev: 0.0006170879573173944",
            "extra": "mean: 48.3454890612494 usec\nrounds: 6445"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 46802.87490839253,
            "unit": "iter/sec",
            "range": "stddev: 0.000009758849929263171",
            "extra": "mean: 21.36620884843729 usec\nrounds: 4046"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 39635.29175692746,
            "unit": "iter/sec",
            "range": "stddev: 0.00045380333673201913",
            "extra": "mean: 25.23004008984543 usec\nrounds: 12447"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21120.255463335372,
            "unit": "iter/sec",
            "range": "stddev: 0.0005494343702001869",
            "extra": "mean: 47.34791213752095 usec\nrounds: 5133"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 41857.744956892566,
            "unit": "iter/sec",
            "range": "stddev: 0.0002962928178768948",
            "extra": "mean: 23.890441327640932 usec\nrounds: 14189"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23772.03219060083,
            "unit": "iter/sec",
            "range": "stddev: 0.00050538475393777",
            "extra": "mean: 42.06623951970702 usec\nrounds: 9160"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19708.542197022118,
            "unit": "iter/sec",
            "range": "stddev: 0.0003793811928557833",
            "extra": "mean: 50.739419993788076 usec\nrounds: 9593"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 21421.2900306105,
            "unit": "iter/sec",
            "range": "stddev: 0.0004257412490567831",
            "extra": "mean: 46.68252932344525 usec\nrounds: 9293"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34115.32105309681,
            "unit": "iter/sec",
            "range": "stddev: 0.0004004832731779844",
            "extra": "mean: 29.31234322677509 usec\nrounds: 13443"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21582.670293038904,
            "unit": "iter/sec",
            "range": "stddev: 0.000520922081283672",
            "extra": "mean: 46.333469696867475 usec\nrounds: 8514"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20724.64799272517,
            "unit": "iter/sec",
            "range": "stddev: 0.0005670517922056581",
            "extra": "mean: 48.251724244051 usec\nrounds: 5193"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 87155.9958947414,
            "unit": "iter/sec",
            "range": "stddev: 0.000008250525613196016",
            "extra": "mean: 11.473679919941521 usec\nrounds: 4477"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 51730.16108983821,
            "unit": "iter/sec",
            "range": "stddev: 0.0005431694959345216",
            "extra": "mean: 19.331082272551402 usec\nrounds: 8800"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 56779.64113197459,
            "unit": "iter/sec",
            "range": "stddev: 0.00045649695373691803",
            "extra": "mean: 17.611946466439804 usec\nrounds: 7584"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 62655.62681507259,
            "unit": "iter/sec",
            "range": "stddev: 0.0003776304248661128",
            "extra": "mean: 15.960258492848366 usec\nrounds: 8066"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 55867.88948383101,
            "unit": "iter/sec",
            "range": "stddev: 0.00041999432422828564",
            "extra": "mean: 17.899369552691173 usec\nrounds: 7298"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 56472.81877226718,
            "unit": "iter/sec",
            "range": "stddev: 0.00037152820039961323",
            "extra": "mean: 17.707633897868806 usec\nrounds: 6968"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37179.09598286853,
            "unit": "iter/sec",
            "range": "stddev: 0.0004342008771506511",
            "extra": "mean: 26.89683472833181 usec\nrounds: 5736"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36253.636239673,
            "unit": "iter/sec",
            "range": "stddev: 0.0003908489426049244",
            "extra": "mean: 27.583440000031842 usec\nrounds: 5950"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38423.34134538703,
            "unit": "iter/sec",
            "range": "stddev: 0.0003704749390690752",
            "extra": "mean: 26.02584691974105 usec\nrounds: 6428"
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
        "date": 1722951557524,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 49574.0351117635,
            "unit": "iter/sec",
            "range": "stddev: 0.0000079753530264901",
            "extra": "mean: 20.17184999658639 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2782.0191005422216,
            "unit": "iter/sec",
            "range": "stddev: 0.0001061796489583877",
            "extra": "mean: 359.451162576525 usec\nrounds: 2079"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 317.7190681468114,
            "unit": "iter/sec",
            "range": "stddev: 0.0003877676646684418",
            "extra": "mean: 3.1474346372497877 msec\nrounds: 306"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.224110463758947,
            "unit": "iter/sec",
            "range": "stddev: 0.0004825984917343119",
            "extra": "mean: 32.02653286666646 msec\nrounds: 30"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15309.214420397411,
            "unit": "iter/sec",
            "range": "stddev: 0.0003559295216542873",
            "extra": "mean: 65.32013809066768 usec\nrounds: 4946"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21589.33037459657,
            "unit": "iter/sec",
            "range": "stddev: 0.0005797272610908785",
            "extra": "mean: 46.31917630834284 usec\nrounds: 5411"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 32328.015597684054,
            "unit": "iter/sec",
            "range": "stddev: 0.0005887394627377382",
            "extra": "mean: 30.93292246715072 usec\nrounds: 3908"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 43790.482577910814,
            "unit": "iter/sec",
            "range": "stddev: 0.00025916449409822874",
            "extra": "mean: 22.83601232804018 usec\nrounds: 9410"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22735.302538904998,
            "unit": "iter/sec",
            "range": "stddev: 0.00037808683706923757",
            "extra": "mean: 43.98445977522334 usec\nrounds: 7893"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 38644.233685062885,
            "unit": "iter/sec",
            "range": "stddev: 0.00039108510541482184",
            "extra": "mean: 25.877081899194938 usec\nrounds: 14591"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 24366.549004736844,
            "unit": "iter/sec",
            "range": "stddev: 0.0005120716927954575",
            "extra": "mean: 41.03986985623612 usec\nrounds: 8967"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18858.04380330044,
            "unit": "iter/sec",
            "range": "stddev: 0.000394174354933064",
            "extra": "mean: 53.02776949881647 usec\nrounds: 9154"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22134.418791499535,
            "unit": "iter/sec",
            "range": "stddev: 0.00042657550307584856",
            "extra": "mean: 45.17850725694402 usec\nrounds: 8956"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 33946.90244637791,
            "unit": "iter/sec",
            "range": "stddev: 0.0003694414055358491",
            "extra": "mean: 29.457768689782135 usec\nrounds: 12667"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 24637.265984737332,
            "unit": "iter/sec",
            "range": "stddev: 0.000009455699093876728",
            "extra": "mean: 40.58891926642733 usec\nrounds: 2019"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20103.010642053883,
            "unit": "iter/sec",
            "range": "stddev: 0.0006867142002180609",
            "extra": "mean: 49.743792997257856 usec\nrounds: 5198"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 59623.7409433791,
            "unit": "iter/sec",
            "range": "stddev: 0.0004354506871943738",
            "extra": "mean: 16.77184262808395 usec\nrounds: 7371"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 86684.5114582146,
            "unit": "iter/sec",
            "range": "stddev: 0.000007869388443407514",
            "extra": "mean: 11.536086241681593 usec\nrounds: 1948"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 58439.714276356644,
            "unit": "iter/sec",
            "range": "stddev: 0.0003871381962113254",
            "extra": "mean: 17.11165108150737 usec\nrounds: 6844"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 54825.09729876546,
            "unit": "iter/sec",
            "range": "stddev: 0.00039320871468375665",
            "extra": "mean: 18.239821710676978 usec\nrounds: 8116"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 54383.51992394303,
            "unit": "iter/sec",
            "range": "stddev: 0.0004351460723659699",
            "extra": "mean: 18.387923426040274 usec\nrounds: 7705"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 55086.693967920066,
            "unit": "iter/sec",
            "range": "stddev: 0.0004168423695744068",
            "extra": "mean: 18.153204121894728 usec\nrounds: 7231"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37397.84886019032,
            "unit": "iter/sec",
            "range": "stddev: 0.00043147023260562843",
            "extra": "mean: 26.739505893465736 usec\nrounds: 5938"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 35659.184529447775,
            "unit": "iter/sec",
            "range": "stddev: 0.0004165992646913186",
            "extra": "mean: 28.04326608125848 usec\nrounds: 6250"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37416.17710030748,
            "unit": "iter/sec",
            "range": "stddev: 0.0004029934826186839",
            "extra": "mean: 26.726407599556236 usec\nrounds: 6342"
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
        "date": 1723043194467,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 50101.398593315935,
            "unit": "iter/sec",
            "range": "stddev: 0.000007528611027556666",
            "extra": "mean: 19.959522649601457 usec\nrounds: 21"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2705.34969001094,
            "unit": "iter/sec",
            "range": "stddev: 0.000118058684564475",
            "extra": "mean: 369.6379819926186 usec\nrounds: 2171"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 314.4726082512406,
            "unit": "iter/sec",
            "range": "stddev: 0.0005561168434879431",
            "extra": "mean: 3.1799271979869013 msec\nrounds: 307"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.77735488630181,
            "unit": "iter/sec",
            "range": "stddev: 0.0006339667697928666",
            "extra": "mean: 31.468950250200578 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15587.01688592389,
            "unit": "iter/sec",
            "range": "stddev: 0.00037903939679344545",
            "extra": "mean: 64.15595795646225 usec\nrounds: 4530"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 23132.72236261341,
            "unit": "iter/sec",
            "range": "stddev: 0.0005147604392541364",
            "extra": "mean: 43.22880741508304 usec\nrounds: 6278"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 37974.186509622225,
            "unit": "iter/sec",
            "range": "stddev: 0.0004637330748884127",
            "extra": "mean: 26.333678003783216 usec\nrounds: 6367"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 43888.01114312847,
            "unit": "iter/sec",
            "range": "stddev: 0.0002807069211301352",
            "extra": "mean: 22.785265815276517 usec\nrounds: 12501"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 23017.88771760498,
            "unit": "iter/sec",
            "range": "stddev: 0.00043087284358015577",
            "extra": "mean: 43.444472936374645 usec\nrounds: 7935"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 40523.60068653592,
            "unit": "iter/sec",
            "range": "stddev: 0.00034003742756157074",
            "extra": "mean: 24.676977935286306 usec\nrounds: 15711"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 25073.575225833425,
            "unit": "iter/sec",
            "range": "stddev: 0.0004884853565850931",
            "extra": "mean: 39.88262507413363 usec\nrounds: 9186"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19181.244564440556,
            "unit": "iter/sec",
            "range": "stddev: 0.0003774923063608765",
            "extra": "mean: 52.1342604563765 usec\nrounds: 8947"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 23013.130019802153,
            "unit": "iter/sec",
            "range": "stddev: 0.000344624599028397",
            "extra": "mean: 43.453454577431586 usec\nrounds: 9650"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34631.73641332073,
            "unit": "iter/sec",
            "range": "stddev: 0.0003336067744797736",
            "extra": "mean: 28.8752486466535 usec\nrounds: 13092"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21966.257986777462,
            "unit": "iter/sec",
            "range": "stddev: 0.0004318544090871044",
            "extra": "mean: 45.52436744583205 usec\nrounds: 9298"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21458.66284546672,
            "unit": "iter/sec",
            "range": "stddev: 0.000557728642123761",
            "extra": "mean: 46.60122614355985 usec\nrounds: 5348"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 62294.211062497256,
            "unit": "iter/sec",
            "range": "stddev: 0.0004298805539548212",
            "extra": "mean: 16.052856002891513 usec\nrounds: 7949"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 68200.86991816848,
            "unit": "iter/sec",
            "range": "stddev: 0.00035932872117268343",
            "extra": "mean: 14.662569571324536 usec\nrounds: 8752"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 61930.762274377455,
            "unit": "iter/sec",
            "range": "stddev: 0.0003703800427905652",
            "extra": "mean: 16.14706429043469 usec\nrounds: 8193"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 56979.09867190999,
            "unit": "iter/sec",
            "range": "stddev: 0.00039716284457461565",
            "extra": "mean: 17.55029516626924 usec\nrounds: 8497"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 58116.85330416509,
            "unit": "iter/sec",
            "range": "stddev: 0.000412204734410727",
            "extra": "mean: 17.20671273729014 usec\nrounds: 8121"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 57414.13319644637,
            "unit": "iter/sec",
            "range": "stddev: 0.0003984205275484861",
            "extra": "mean: 17.417314245230035 usec\nrounds: 7676"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38361.486203740315,
            "unit": "iter/sec",
            "range": "stddev: 0.0004329013561738601",
            "extra": "mean: 26.06781172890268 usec\nrounds: 5966"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 33868.659217963956,
            "unit": "iter/sec",
            "range": "stddev: 0.0004882844496860432",
            "extra": "mean: 29.5258218981872 usec\nrounds: 4091"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 40434.45544440794,
            "unit": "iter/sec",
            "range": "stddev: 0.0003285995810128856",
            "extra": "mean: 24.731382901270145 usec\nrounds: 6979"
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
        "date": 1723043468966,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47162.357711706434,
            "unit": "iter/sec",
            "range": "stddev: 0.000008206732306229746",
            "extra": "mean: 21.203350479481742 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2930.141517435511,
            "unit": "iter/sec",
            "range": "stddev: 0.00006886844496202359",
            "extra": "mean: 341.28044466439627 usec\nrounds: 2211"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 317.15303334973953,
            "unit": "iter/sec",
            "range": "stddev: 0.0003877365253604823",
            "extra": "mean: 3.1530519807365454 msec\nrounds: 303"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.427642169598844,
            "unit": "iter/sec",
            "range": "stddev: 0.00042743752236340066",
            "extra": "mean: 31.81912262471087 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14655.209098285783,
            "unit": "iter/sec",
            "range": "stddev: 0.000469590937917061",
            "extra": "mean: 68.23512331304573 usec\nrounds: 5532"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21893.87535237274,
            "unit": "iter/sec",
            "range": "stddev: 0.0006332215738819447",
            "extra": "mean: 45.67487408717824 usec\nrounds: 6645"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 35844.4426395645,
            "unit": "iter/sec",
            "range": "stddev: 0.0005675990491696519",
            "extra": "mean: 27.898327505202065 usec\nrounds: 5947"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 41071.1238770116,
            "unit": "iter/sec",
            "range": "stddev: 0.0003600720798463688",
            "extra": "mean: 24.348006716215565 usec\nrounds: 12113"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22842.46812289896,
            "unit": "iter/sec",
            "range": "stddev: 0.0004796663751395837",
            "extra": "mean: 43.778106403376206 usec\nrounds: 9592"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39397.65520387741,
            "unit": "iter/sec",
            "range": "stddev: 0.0003855466997991295",
            "extra": "mean: 25.382221221672676 usec\nrounds: 15185"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 28121.672117151465,
            "unit": "iter/sec",
            "range": "stddev: 0.000011263976861348297",
            "extra": "mean: 35.559763154698686 usec\nrounds: 5176"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 17503.579583342696,
            "unit": "iter/sec",
            "range": "stddev: 0.0006675223804005509",
            "extra": "mean: 57.131171097805115 usec\nrounds: 6863"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22208.979922992974,
            "unit": "iter/sec",
            "range": "stddev: 0.0004080077695558142",
            "extra": "mean: 45.026831645009466 usec\nrounds: 7455"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 35293.35833490441,
            "unit": "iter/sec",
            "range": "stddev: 0.0003483769216365924",
            "extra": "mean: 28.33394290537153 usec\nrounds: 13761"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 22329.85841551519,
            "unit": "iter/sec",
            "range": "stddev: 0.0004745189686744612",
            "extra": "mean: 44.78308735290421 usec\nrounds: 9077"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21352.13961045478,
            "unit": "iter/sec",
            "range": "stddev: 0.0005007296865853498",
            "extra": "mean: 46.83371400917423 usec\nrounds: 5479"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 58950.52860399102,
            "unit": "iter/sec",
            "range": "stddev: 0.00047734360902726826",
            "extra": "mean: 16.963376303504404 usec\nrounds: 7729"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 66098.7518669182,
            "unit": "iter/sec",
            "range": "stddev: 0.00034281754724534993",
            "extra": "mean: 15.12887871186098 usec\nrounds: 8047"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 53890.842436669554,
            "unit": "iter/sec",
            "range": "stddev: 0.00040282183420593635",
            "extra": "mean: 18.556028348882492 usec\nrounds: 8146"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 63077.953174691385,
            "unit": "iter/sec",
            "range": "stddev: 0.0003671619410404139",
            "extra": "mean: 15.853399637596794 usec\nrounds: 8926"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 47794.05942623754,
            "unit": "iter/sec",
            "range": "stddev: 0.0005279855489568786",
            "extra": "mean: 20.92310241073662 usec\nrounds: 4372"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 75360.77468261348,
            "unit": "iter/sec",
            "range": "stddev: 0.000007730411516691463",
            "extra": "mean: 13.269502658532389 usec\nrounds: 4745"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36145.771683306775,
            "unit": "iter/sec",
            "range": "stddev: 0.0004736439348240771",
            "extra": "mean: 27.66575323834712 usec\nrounds: 4730"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 38402.989801064985,
            "unit": "iter/sec",
            "range": "stddev: 0.0003272194663039919",
            "extra": "mean: 26.03963923590835 usec\nrounds: 6538"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 35077.22048729405,
            "unit": "iter/sec",
            "range": "stddev: 0.00047802695071566884",
            "extra": "mean: 28.50853021157215 usec\nrounds: 4005"
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
        "date": 1723106272718,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 49628.0480451116,
            "unit": "iter/sec",
            "range": "stddev: 0.000008093267315754934",
            "extra": "mean: 20.149895863141865 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2780.41952168117,
            "unit": "iter/sec",
            "range": "stddev: 0.00008014656313473175",
            "extra": "mean: 359.6579552841558 usec\nrounds: 1959"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 310.7680799028081,
            "unit": "iter/sec",
            "range": "stddev: 0.00029636348286478647",
            "extra": "mean: 3.2178336987271905 msec\nrounds: 292"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 30.228473447598766,
            "unit": "iter/sec",
            "range": "stddev: 0.0006100569700041971",
            "extra": "mean: 33.08139267216076 msec\nrounds: 31"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14337.941600135051,
            "unit": "iter/sec",
            "range": "stddev: 0.0004871938513666955",
            "extra": "mean: 69.74501834981535 usec\nrounds: 5520"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22315.887079452557,
            "unit": "iter/sec",
            "range": "stddev: 0.0006665624894229911",
            "extra": "mean: 44.81112475787503 usec\nrounds: 5451"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 38025.38218225527,
            "unit": "iter/sec",
            "range": "stddev: 0.0004355502747009529",
            "extra": "mean: 26.29822351835966 usec\nrounds: 5902"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 42696.00691299394,
            "unit": "iter/sec",
            "range": "stddev: 0.00028209118747857395",
            "extra": "mean: 23.421393996815752 usec\nrounds: 11878"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22520.976493465932,
            "unit": "iter/sec",
            "range": "stddev: 0.00042560668578309934",
            "extra": "mean: 44.40304798906622 usec\nrounds: 7685"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39147.1951067385,
            "unit": "iter/sec",
            "range": "stddev: 0.00036546111919134514",
            "extra": "mean: 25.54461430182689 usec\nrounds: 14463"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 24613.368682764238,
            "unit": "iter/sec",
            "range": "stddev: 0.00047695916937803086",
            "extra": "mean: 40.62832734879807 usec\nrounds: 9309"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18697.617019349604,
            "unit": "iter/sec",
            "range": "stddev: 0.00039754729971570694",
            "extra": "mean: 53.48275124927042 usec\nrounds: 8588"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22377.19065829147,
            "unit": "iter/sec",
            "range": "stddev: 0.00040734108277412705",
            "extra": "mean: 44.688362148331954 usec\nrounds: 9622"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34258.00139543851,
            "unit": "iter/sec",
            "range": "stddev: 0.0003615348959875668",
            "extra": "mean: 29.190260939540718 usec\nrounds: 13181"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 19998.868031182883,
            "unit": "iter/sec",
            "range": "stddev: 0.0006320440214456544",
            "extra": "mean: 50.00283008222103 usec\nrounds: 4809"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 23330.805503127882,
            "unit": "iter/sec",
            "range": "stddev: 0.0003833375355626898",
            "extra": "mean: 42.861786313633 usec\nrounds: 4482"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 64067.89398947236,
            "unit": "iter/sec",
            "range": "stddev: 0.0003703010755173998",
            "extra": "mean: 15.608441884547041 usec\nrounds: 7653"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 60702.29541600549,
            "unit": "iter/sec",
            "range": "stddev: 0.0003657163257035082",
            "extra": "mean: 16.473841609230615 usec\nrounds: 8942"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 60242.0585788339,
            "unit": "iter/sec",
            "range": "stddev: 0.00039141011656170036",
            "extra": "mean: 16.599698343498357 usec\nrounds: 8361"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 63081.0131063789,
            "unit": "iter/sec",
            "range": "stddev: 0.0003619603753559973",
            "extra": "mean: 15.852630621413999 usec\nrounds: 8720"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 50037.49982892159,
            "unit": "iter/sec",
            "range": "stddev: 0.00044308011852960046",
            "extra": "mean: 19.985011309897654 usec\nrounds: 7609"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 55456.47621499268,
            "unit": "iter/sec",
            "range": "stddev: 0.00043573255229686686",
            "extra": "mean: 18.032159059714104 usec\nrounds: 7742"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36713.50730970719,
            "unit": "iter/sec",
            "range": "stddev: 0.00048522916444195896",
            "extra": "mean: 27.237931575542945 usec\nrounds: 5799"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36117.80681066331,
            "unit": "iter/sec",
            "range": "stddev: 0.000408708877558221",
            "extra": "mean: 27.687173953894764 usec\nrounds: 6240"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37428.19742330211,
            "unit": "iter/sec",
            "range": "stddev: 0.0004300528444762283",
            "extra": "mean: 26.717824229959263 usec\nrounds: 6258"
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
        "date": 1723197930383,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 45767.70966402979,
            "unit": "iter/sec",
            "range": "stddev: 0.000009456090389634605",
            "extra": "mean: 21.849465645992986 usec\nrounds: 13"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2978.3717509511393,
            "unit": "iter/sec",
            "range": "stddev: 0.0000625867266005014",
            "extra": "mean: 335.75392315638607 usec\nrounds: 1918"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 321.12262337663304,
            "unit": "iter/sec",
            "range": "stddev: 0.0004012219376334224",
            "extra": "mean: 3.1140752074236024 msec\nrounds: 314"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.744208346150263,
            "unit": "iter/sec",
            "range": "stddev: 0.0005410538958489266",
            "extra": "mean: 31.5018093724575 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14881.011173176024,
            "unit": "iter/sec",
            "range": "stddev: 0.0004121147510839343",
            "extra": "mean: 67.19973450477372 usec\nrounds: 4257"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22192.33384596575,
            "unit": "iter/sec",
            "range": "stddev: 0.000528769890119094",
            "extra": "mean: 45.060605474885 usec\nrounds: 6275"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 36775.77329431573,
            "unit": "iter/sec",
            "range": "stddev: 0.0004846005340246243",
            "extra": "mean: 27.191814350089153 usec\nrounds: 6249"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 41279.4130808731,
            "unit": "iter/sec",
            "range": "stddev: 0.00031851148475146916",
            "extra": "mean: 24.225150634793113 usec\nrounds: 10976"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21529.909106707997,
            "unit": "iter/sec",
            "range": "stddev: 0.000507218187196915",
            "extra": "mean: 46.44701447849743 usec\nrounds: 5451"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39655.17904150515,
            "unit": "iter/sec",
            "range": "stddev: 0.0003678739526703683",
            "extra": "mean: 25.217387089674933 usec\nrounds: 6222"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 25533.316889307804,
            "unit": "iter/sec",
            "range": "stddev: 0.00037352656763253484",
            "extra": "mean: 39.16451608442438 usec\nrounds: 8375"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18556.331144584103,
            "unit": "iter/sec",
            "range": "stddev: 0.00047578431101822835",
            "extra": "mean: 53.88996306480888 usec\nrounds: 4815"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22795.858283132573,
            "unit": "iter/sec",
            "range": "stddev: 0.00031186033517277355",
            "extra": "mean: 43.867617861966345 usec\nrounds: 8828"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 33907.723230948075,
            "unit": "iter/sec",
            "range": "stddev: 0.0003475685555695656",
            "extra": "mean: 29.49180613481254 usec\nrounds: 13145"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20987.27090913961,
            "unit": "iter/sec",
            "range": "stddev: 0.0005060290992160988",
            "extra": "mean: 47.64792927719423 usec\nrounds: 8537"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 22889.255266816228,
            "unit": "iter/sec",
            "range": "stddev: 0.0004695488220252083",
            "extra": "mean: 43.688621073213916 usec\nrounds: 5533"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 61555.3749371968,
            "unit": "iter/sec",
            "range": "stddev: 0.00040376293884886367",
            "extra": "mean: 16.24553503281024 usec\nrounds: 7898"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 58471.46620335864,
            "unit": "iter/sec",
            "range": "stddev: 0.0003756700611841716",
            "extra": "mean: 17.102358892833088 usec\nrounds: 8717"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 57845.4701024809,
            "unit": "iter/sec",
            "range": "stddev: 0.00040782895234679355",
            "extra": "mean: 17.28743838071275 usec\nrounds: 8289"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 62729.128145250266,
            "unit": "iter/sec",
            "range": "stddev: 0.0003575729066573869",
            "extra": "mean: 15.94155744815207 usec\nrounds: 8221"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 54431.24406945211,
            "unit": "iter/sec",
            "range": "stddev: 0.00040478234003297944",
            "extra": "mean: 18.371801289789367 usec\nrounds: 5923"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 57560.51314178095,
            "unit": "iter/sec",
            "range": "stddev: 0.0003456598170090206",
            "extra": "mean: 17.37302093775357 usec\nrounds: 7470"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38009.54381943562,
            "unit": "iter/sec",
            "range": "stddev: 0.00039337267467316707",
            "extra": "mean: 26.309181839974226 usec\nrounds: 6003"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37045.587205942866,
            "unit": "iter/sec",
            "range": "stddev: 0.00036093067128560287",
            "extra": "mean: 26.993768365468902 usec\nrounds: 6246"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 34635.25215362197,
            "unit": "iter/sec",
            "range": "stddev: 0.00046725056149698893",
            "extra": "mean: 28.872317590314566 usec\nrounds: 3950"
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
        "date": 1723200229360,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 25296.98051725296,
            "unit": "iter/sec",
            "range": "stddev: 0.000014453649630688707",
            "extra": "mean: 39.53040954109063 usec\nrounds: 17"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2800.603027950472,
            "unit": "iter/sec",
            "range": "stddev: 0.0001022165849933757",
            "extra": "mean: 357.0659568742295 usec\nrounds: 1094"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 311.0065335824809,
            "unit": "iter/sec",
            "range": "stddev: 0.000595984691793496",
            "extra": "mean: 3.2153665342043163 msec\nrounds: 298"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 30.977974628803445,
            "unit": "iter/sec",
            "range": "stddev: 0.0011362095565733525",
            "extra": "mean: 32.28100003252621 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14436.369967705352,
            "unit": "iter/sec",
            "range": "stddev: 0.0005377565440428116",
            "extra": "mean: 69.2694910311272 usec\nrounds: 5529"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22581.89183543264,
            "unit": "iter/sec",
            "range": "stddev: 0.0006690632531121815",
            "extra": "mean: 44.283269412836646 usec\nrounds: 5567"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 37903.74534497977,
            "unit": "iter/sec",
            "range": "stddev: 0.00044421308575771993",
            "extra": "mean: 26.38261709755938 usec\nrounds: 6009"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 42588.21231992161,
            "unit": "iter/sec",
            "range": "stddev: 0.00030245733983630846",
            "extra": "mean: 23.480675650060736 usec\nrounds: 11613"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22216.05791458231,
            "unit": "iter/sec",
            "range": "stddev: 0.00044988078943059495",
            "extra": "mean: 45.0124861865621 usec\nrounds: 6921"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 38922.8811527068,
            "unit": "iter/sec",
            "range": "stddev: 0.00038230765695451224",
            "extra": "mean: 25.691828826254742 usec\nrounds: 14971"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23871.526016186017,
            "unit": "iter/sec",
            "range": "stddev: 0.0005642668666597238",
            "extra": "mean: 41.89091218223556 usec\nrounds: 8633"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19573.27736114608,
            "unit": "iter/sec",
            "range": "stddev: 0.0003712299421189999",
            "extra": "mean: 51.09006435401816 usec\nrounds: 8003"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 21822.30269457175,
            "unit": "iter/sec",
            "range": "stddev: 0.0004053635385830591",
            "extra": "mean: 45.82467826590764 usec\nrounds: 8912"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34499.36526118233,
            "unit": "iter/sec",
            "range": "stddev: 0.00038987051132387886",
            "extra": "mean: 28.98604053811885 usec\nrounds: 13766"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 22103.537429183798,
            "unit": "iter/sec",
            "range": "stddev: 0.0004715190701252306",
            "extra": "mean: 45.24162719220126 usec\nrounds: 8981"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21226.577417622426,
            "unit": "iter/sec",
            "range": "stddev: 0.000547409291844277",
            "extra": "mean: 47.110750844353944 usec\nrounds: 5141"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 64318.38556517985,
            "unit": "iter/sec",
            "range": "stddev: 0.0004172320642551721",
            "extra": "mean: 15.547653928387335 usec\nrounds: 8720"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 66731.82228780998,
            "unit": "iter/sec",
            "range": "stddev: 0.0003655623956134597",
            "extra": "mean: 14.985354298988952 usec\nrounds: 8548"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 52483.88186474485,
            "unit": "iter/sec",
            "range": "stddev: 0.00044457053285516037",
            "extra": "mean: 19.053468693056658 usec\nrounds: 7958"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 64367.58853724601,
            "unit": "iter/sec",
            "range": "stddev: 0.0003837017183705102",
            "extra": "mean: 15.535769208152864 usec\nrounds: 9030"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 58092.18090476063,
            "unit": "iter/sec",
            "range": "stddev: 0.00040144949901665803",
            "extra": "mean: 17.21402062076913 usec\nrounds: 7631"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 56670.87330812358,
            "unit": "iter/sec",
            "range": "stddev: 0.0004103556989949863",
            "extra": "mean: 17.645748894020546 usec\nrounds: 6749"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38118.851055888146,
            "unit": "iter/sec",
            "range": "stddev: 0.00040868374552473284",
            "extra": "mean: 26.23373927335441 usec\nrounds: 5861"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37193.64370390599,
            "unit": "iter/sec",
            "range": "stddev: 0.0003964825542419573",
            "extra": "mean: 26.886314445577764 usec\nrounds: 6034"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 39231.53256947447,
            "unit": "iter/sec",
            "range": "stddev: 0.0003686093080680722",
            "extra": "mean: 25.489700108684683 usec\nrounds: 6825"
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
        "date": 1723715810735,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 22822.710659699285,
            "unit": "iter/sec",
            "range": "stddev: 0.000013328362063973624",
            "extra": "mean: 43.81600480813246 usec\nrounds: 13"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2667.648893675763,
            "unit": "iter/sec",
            "range": "stddev: 0.00011572110701649346",
            "extra": "mean: 374.86192518465066 usec\nrounds: 1078"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 319.8533392787846,
            "unit": "iter/sec",
            "range": "stddev: 0.0001610523957830524",
            "extra": "mean: 3.126432890320394 msec\nrounds: 293"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.002769929103188,
            "unit": "iter/sec",
            "range": "stddev: 0.0005764027157547398",
            "extra": "mean: 32.255182433272566 msec\nrounds: 31"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15509.939817819824,
            "unit": "iter/sec",
            "range": "stddev: 0.00035378983986764285",
            "extra": "mean: 64.4747827358473 usec\nrounds: 5038"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21823.15485343286,
            "unit": "iter/sec",
            "range": "stddev: 0.0005805811940418048",
            "extra": "mean: 45.8228888864204 usec\nrounds: 5809"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 38184.41867676379,
            "unit": "iter/sec",
            "range": "stddev: 0.000444833812711712",
            "extra": "mean: 26.188692525742862 usec\nrounds: 6577"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 42625.89870990189,
            "unit": "iter/sec",
            "range": "stddev: 0.0002869704782997696",
            "extra": "mean: 23.45991592589466 usec\nrounds: 11902"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 23404.54096282185,
            "unit": "iter/sec",
            "range": "stddev: 0.00039664190340489916",
            "extra": "mean: 42.726751256882224 usec\nrounds: 8729"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39762.282544394104,
            "unit": "iter/sec",
            "range": "stddev: 0.00034827850356887344",
            "extra": "mean: 25.14946165083738 usec\nrounds: 15429"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23232.32244257506,
            "unit": "iter/sec",
            "range": "stddev: 0.0005929565415641347",
            "extra": "mean: 43.043479724068455 usec\nrounds: 5432"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19942.221021416208,
            "unit": "iter/sec",
            "range": "stddev: 0.00030332929375529556",
            "extra": "mean: 50.14486595681028 usec\nrounds: 7869"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 21801.072115093823,
            "unit": "iter/sec",
            "range": "stddev: 0.00040785919709521493",
            "extra": "mean: 45.869303799406126 usec\nrounds: 9270"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 35015.72783379561,
            "unit": "iter/sec",
            "range": "stddev: 0.00036727486399793055",
            "extra": "mean: 28.558595290281097 usec\nrounds: 14702"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21426.84288724374,
            "unit": "iter/sec",
            "range": "stddev: 0.0005308449264641757",
            "extra": "mean: 46.670431349237184 usec\nrounds: 7733"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21135.15838433788,
            "unit": "iter/sec",
            "range": "stddev: 0.000559148357249026",
            "extra": "mean: 47.3145259578961 usec\nrounds: 5152"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 61911.13492462097,
            "unit": "iter/sec",
            "range": "stddev: 0.00045808647655070094",
            "extra": "mean: 16.152183306242662 usec\nrounds: 8717"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 65249.49718507188,
            "unit": "iter/sec",
            "range": "stddev: 0.0003905965629805426",
            "extra": "mean: 15.32578859824203 usec\nrounds: 8345"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 58821.1180546925,
            "unit": "iter/sec",
            "range": "stddev: 0.0004083734153259441",
            "extra": "mean: 17.00069691076238 usec\nrounds: 7720"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 63778.17996226738,
            "unit": "iter/sec",
            "range": "stddev: 0.0003347588529217874",
            "extra": "mean: 15.679343634321688 usec\nrounds: 7597"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 51343.101621389265,
            "unit": "iter/sec",
            "range": "stddev: 0.0004158522554485542",
            "extra": "mean: 19.47681321191171 usec\nrounds: 7963"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 56717.59206219684,
            "unit": "iter/sec",
            "range": "stddev: 0.0003966553994750654",
            "extra": "mean: 17.63121394334573 usec\nrounds: 8016"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36809.198370205806,
            "unit": "iter/sec",
            "range": "stddev: 0.00046016723377319035",
            "extra": "mean: 27.16712246603617 usec\nrounds: 5401"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36193.499939835594,
            "unit": "iter/sec",
            "range": "stddev: 0.0004067257757859753",
            "extra": "mean: 27.62927049504189 usec\nrounds: 6354"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37555.550941123314,
            "unit": "iter/sec",
            "range": "stddev: 0.0004319178657881488",
            "extra": "mean: 26.627222206584655 usec\nrounds: 6600"
          }
        ]
      }
    ]
  }
}