window.BENCHMARK_DATA = {
  "lastUpdate": 1756230318650,
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
        "date": 1723742065901,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 46243.33939388284,
            "unit": "iter/sec",
            "range": "stddev: 0.00000988501199426779",
            "extra": "mean: 21.624735866983734 usec\nrounds: 15"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2693.9665897333357,
            "unit": "iter/sec",
            "range": "stddev: 0.00012054259489748777",
            "extra": "mean: 371.1998522219928 usec\nrounds: 1177"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 320.5496296008698,
            "unit": "iter/sec",
            "range": "stddev: 0.00023338948593449232",
            "extra": "mean: 3.119641726758952 msec\nrounds: 300"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.947412459021045,
            "unit": "iter/sec",
            "range": "stddev: 0.0004889115804351184",
            "extra": "mean: 31.301439554226818 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15630.778649526166,
            "unit": "iter/sec",
            "range": "stddev: 0.00035437091157633873",
            "extra": "mean: 63.97633940202422 usec\nrounds: 5395"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22556.73407701447,
            "unit": "iter/sec",
            "range": "stddev: 0.000549677428846479",
            "extra": "mean: 44.332659000445005 usec\nrounds: 5946"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 38228.07084978774,
            "unit": "iter/sec",
            "range": "stddev: 0.0004521405483794877",
            "extra": "mean: 26.158787973616835 usec\nrounds: 5668"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 43840.52191807471,
            "unit": "iter/sec",
            "range": "stddev: 0.00027560945017993387",
            "extra": "mean: 22.809947424182397 usec\nrounds: 12047"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22264.522447732295,
            "unit": "iter/sec",
            "range": "stddev: 0.0004254473370648138",
            "extra": "mean: 44.91450478435269 usec\nrounds: 9076"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 42704.621458720096,
            "unit": "iter/sec",
            "range": "stddev: 0.0003255647601665219",
            "extra": "mean: 23.41666934026421 usec\nrounds: 15953"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 24284.730950724537,
            "unit": "iter/sec",
            "range": "stddev: 0.0004996233291300428",
            "extra": "mean: 41.17813790192166 usec\nrounds: 9734"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18598.437005211235,
            "unit": "iter/sec",
            "range": "stddev: 0.0005037014435862395",
            "extra": "mean: 53.767959088164375 usec\nrounds: 5109"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 25355.091471978947,
            "unit": "iter/sec",
            "range": "stddev: 0.000010531315340897838",
            "extra": "mean: 39.43981038700432 usec\nrounds: 4873"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 35910.21173741994,
            "unit": "iter/sec",
            "range": "stddev: 0.0003323565770280791",
            "extra": "mean: 27.847232071816453 usec\nrounds: 14091"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 22059.7064602959,
            "unit": "iter/sec",
            "range": "stddev: 0.0004200184366209026",
            "extra": "mean: 45.33151888488848 usec\nrounds: 9774"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21600.948374058393,
            "unit": "iter/sec",
            "range": "stddev: 0.0005510459754847472",
            "extra": "mean: 46.29426369079923 usec\nrounds: 5599"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 89551.70259178021,
            "unit": "iter/sec",
            "range": "stddev: 0.000007738896302935754",
            "extra": "mean: 11.166733529997543 usec\nrounds: 4563"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 54148.73632588205,
            "unit": "iter/sec",
            "range": "stddev: 0.0005213011737679757",
            "extra": "mean: 18.46765165454137 usec\nrounds: 8377"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 61010.49858712624,
            "unit": "iter/sec",
            "range": "stddev: 0.0003869826452951631",
            "extra": "mean: 16.390621666071894 usec\nrounds: 8290"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 63321.53379769986,
            "unit": "iter/sec",
            "range": "stddev: 0.00037060090767842825",
            "extra": "mean: 15.792415944863368 usec\nrounds: 7484"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 60086.908486627966,
            "unit": "iter/sec",
            "range": "stddev: 0.00035256799954373747",
            "extra": "mean: 16.642560337790467 usec\nrounds: 7903"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 58729.15786082936,
            "unit": "iter/sec",
            "range": "stddev: 0.00037150836388285836",
            "extra": "mean: 17.027317203657216 usec\nrounds: 7855"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 39007.047265374036,
            "unit": "iter/sec",
            "range": "stddev: 0.0003770156434991841",
            "extra": "mean: 25.636393167541414 usec\nrounds: 6116"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 38313.765940255194,
            "unit": "iter/sec",
            "range": "stddev: 0.0003556549215321758",
            "extra": "mean: 26.10027950683199 usec\nrounds: 6303"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38826.00627828257,
            "unit": "iter/sec",
            "range": "stddev: 0.00037449444826895083",
            "extra": "mean: 25.755932578606537 usec\nrounds: 6363"
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
        "date": 1726501427420,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 44368.5365015712,
            "unit": "iter/sec",
            "range": "stddev: 0.000009615861825838779",
            "extra": "mean: 22.5384941413289 usec\nrounds: 21"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2988.528259798299,
            "unit": "iter/sec",
            "range": "stddev: 0.00003566044141792411",
            "extra": "mean: 334.61286394778534 usec\nrounds: 2140"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 304.4808620306698,
            "unit": "iter/sec",
            "range": "stddev: 0.0005124048796678788",
            "extra": "mean: 3.2842786680604963 msec\nrounds: 185"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 29.904881299865078,
            "unit": "iter/sec",
            "range": "stddev: 0.0019020728653720879",
            "extra": "mean: 33.439356938845684 msec\nrounds: 31"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14872.26500912987,
            "unit": "iter/sec",
            "range": "stddev: 0.00042600432364853653",
            "extra": "mean: 67.23925369714125 usec\nrounds: 4767"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21740.4342205232,
            "unit": "iter/sec",
            "range": "stddev: 0.0005983402251687276",
            "extra": "mean: 45.99724135482029 usec\nrounds: 5963"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 36846.39302203923,
            "unit": "iter/sec",
            "range": "stddev: 0.000489109646064702",
            "extra": "mean: 27.139698569731426 usec\nrounds: 6181"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 41676.389088594624,
            "unit": "iter/sec",
            "range": "stddev: 0.0003005222165457323",
            "extra": "mean: 23.99440119138501 usec\nrounds: 11799"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21356.316828732713,
            "unit": "iter/sec",
            "range": "stddev: 0.0004763814491311586",
            "extra": "mean: 46.824553504216766 usec\nrounds: 9075"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 41218.51994302206,
            "unit": "iter/sec",
            "range": "stddev: 0.0003589823452894305",
            "extra": "mean: 24.260939048329202 usec\nrounds: 16208"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 22818.419450324098,
            "unit": "iter/sec",
            "range": "stddev: 0.000569893576669534",
            "extra": "mean: 43.82424480262574 usec\nrounds: 9218"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19209.941922225622,
            "unit": "iter/sec",
            "range": "stddev: 0.00040297705552359484",
            "extra": "mean: 52.05637810091527 usec\nrounds: 9332"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20337.794626378738,
            "unit": "iter/sec",
            "range": "stddev: 0.0005411525265376548",
            "extra": "mean: 49.169539685633836 usec\nrounds: 4514"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34396.70376152858,
            "unit": "iter/sec",
            "range": "stddev: 0.0003262429397259653",
            "extra": "mean: 29.072553199660444 usec\nrounds: 12760"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21214.384570675225,
            "unit": "iter/sec",
            "range": "stddev: 0.0005395838462772568",
            "extra": "mean: 47.13782748061927 usec\nrounds: 7283"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 22355.61094887594,
            "unit": "iter/sec",
            "range": "stddev: 0.0004816420203244282",
            "extra": "mean: 44.73149950081238 usec\nrounds: 4538"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 55082.57557948204,
            "unit": "iter/sec",
            "range": "stddev: 0.0004416356297530523",
            "extra": "mean: 18.15456139223262 usec\nrounds: 8539"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 61223.33688438534,
            "unit": "iter/sec",
            "range": "stddev: 0.0004493019895956919",
            "extra": "mean: 16.333640910302037 usec\nrounds: 8092"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 56928.6158738143,
            "unit": "iter/sec",
            "range": "stddev: 0.0004333526907108838",
            "extra": "mean: 17.56585830606808 usec\nrounds: 7510"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 62845.054459708364,
            "unit": "iter/sec",
            "range": "stddev: 0.0003706727552019489",
            "extra": "mean: 15.912151061005549 usec\nrounds: 8384"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 55567.553596960686,
            "unit": "iter/sec",
            "range": "stddev: 0.00040758321050540964",
            "extra": "mean: 17.99611347393735 usec\nrounds: 6608"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 49792.208783194175,
            "unit": "iter/sec",
            "range": "stddev: 0.00045991741775217954",
            "extra": "mean: 20.08346334572567 usec\nrounds: 4633"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38055.14638647337,
            "unit": "iter/sec",
            "range": "stddev: 0.0003903777306576462",
            "extra": "mean: 26.277654797182656 usec\nrounds: 5373"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37077.38675159666,
            "unit": "iter/sec",
            "range": "stddev: 0.00040121909986092283",
            "extra": "mean: 26.97061706909366 usec\nrounds: 6362"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 36629.0965349718,
            "unit": "iter/sec",
            "range": "stddev: 0.0004431102885480202",
            "extra": "mean: 27.30070066143306 usec\nrounds: 6352"
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
        "date": 1726502800855,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 46573.11289080808,
            "unit": "iter/sec",
            "range": "stddev: 0.000008302350498860774",
            "extra": "mean: 21.47161608768834 usec\nrounds: 18"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 3057.7205654748896,
            "unit": "iter/sec",
            "range": "stddev: 0.000028530286448673358",
            "extra": "mean: 327.0410027950647 usec\nrounds: 2095"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 316.16656928013475,
            "unit": "iter/sec",
            "range": "stddev: 0.0005577684545354483",
            "extra": "mean: 3.1628897459869156 msec\nrounds: 302"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.813266878739785,
            "unit": "iter/sec",
            "range": "stddev: 0.0005824680215816014",
            "extra": "mean: 31.43342693510931 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15129.179398977185,
            "unit": "iter/sec",
            "range": "stddev: 0.000400286486385279",
            "extra": "mean: 66.09743817748671 usec\nrounds: 4694"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 19940.73352282164,
            "unit": "iter/sec",
            "range": "stddev: 0.0007051337335825019",
            "extra": "mean: 50.14860656231762 usec\nrounds: 3996"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 37844.14475051901,
            "unit": "iter/sec",
            "range": "stddev: 0.00045347492636021715",
            "extra": "mean: 26.42416697727819 usec\nrounds: 5850"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 44980.81966524786,
            "unit": "iter/sec",
            "range": "stddev: 0.00028128937007179753",
            "extra": "mean: 22.231698031341104 usec\nrounds: 11515"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21856.759722868865,
            "unit": "iter/sec",
            "range": "stddev: 0.0004517243201251253",
            "extra": "mean: 45.75243598225101 usec\nrounds: 8809"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39457.80221714036,
            "unit": "iter/sec",
            "range": "stddev: 0.0004006085421162773",
            "extra": "mean: 25.343530146380093 usec\nrounds: 12141"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 24732.36965821806,
            "unit": "iter/sec",
            "range": "stddev: 0.0004492577641072293",
            "extra": "mean: 40.43284221525132 usec\nrounds: 8566"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19414.373166015168,
            "unit": "iter/sec",
            "range": "stddev: 0.00037934253701178325",
            "extra": "mean: 51.508230085455374 usec\nrounds: 8516"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20886.170454166,
            "unit": "iter/sec",
            "range": "stddev: 0.00044232646692697917",
            "extra": "mean: 47.87857123901513 usec\nrounds: 7279"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 33944.58105356957,
            "unit": "iter/sec",
            "range": "stddev: 0.0003849616023599556",
            "extra": "mean: 29.45978323968271 usec\nrounds: 13593"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21805.09122636401,
            "unit": "iter/sec",
            "range": "stddev: 0.0005009373818413877",
            "extra": "mean: 45.86084917594494 usec\nrounds: 9304"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21376.45672243292,
            "unit": "iter/sec",
            "range": "stddev: 0.0005812566102785725",
            "extra": "mean: 46.78043760875386 usec\nrounds: 3176"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 63578.614972271236,
            "unit": "iter/sec",
            "range": "stddev: 0.0003633047318746146",
            "extra": "mean: 15.72855905143787 usec\nrounds: 6624"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 66810.9236462914,
            "unit": "iter/sec",
            "range": "stddev: 0.00033515575348718753",
            "extra": "mean: 14.967612261943469 usec\nrounds: 7397"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 60460.55728703672,
            "unit": "iter/sec",
            "range": "stddev: 0.0003757512897560617",
            "extra": "mean: 16.539708611227258 usec\nrounds: 7331"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 56367.3877671636,
            "unit": "iter/sec",
            "range": "stddev: 0.0004024423371581252",
            "extra": "mean: 17.740754709632697 usec\nrounds: 8472"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 54932.05937829515,
            "unit": "iter/sec",
            "range": "stddev: 0.00046581984465728755",
            "extra": "mean: 18.204305669907612 usec\nrounds: 7356"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 57548.512462938634,
            "unit": "iter/sec",
            "range": "stddev: 0.000395651142568661",
            "extra": "mean: 17.376643760236238 usec\nrounds: 7543"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 35046.685139187386,
            "unit": "iter/sec",
            "range": "stddev: 0.0005309643120420704",
            "extra": "mean: 28.533369019880627 usec\nrounds: 5123"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36873.26564074115,
            "unit": "iter/sec",
            "range": "stddev: 0.0004049083445626463",
            "extra": "mean: 27.119919611760757 usec\nrounds: 6162"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37388.66005602862,
            "unit": "iter/sec",
            "range": "stddev: 0.00043972350647446197",
            "extra": "mean: 26.746077513916102 usec\nrounds: 6113"
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
        "date": 1728908652423,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47371.95803273178,
            "unit": "iter/sec",
            "range": "stddev: 0.000007161094086901524",
            "extra": "mean: 21.109534871010553 usec\nrounds: 21"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2555.6363315597737,
            "unit": "iter/sec",
            "range": "stddev: 0.00014374958765935893",
            "extra": "mean: 391.29197986854143 usec\nrounds: 1971"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 330.4368973936571,
            "unit": "iter/sec",
            "range": "stddev: 0.00008648832794395375",
            "extra": "mean: 3.0262964211550414 msec\nrounds: 306"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 32.64853348157561,
            "unit": "iter/sec",
            "range": "stddev: 0.00042290350630990896",
            "extra": "mean: 30.629247116545837 msec\nrounds: 33"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15030.368569637882,
            "unit": "iter/sec",
            "range": "stddev: 0.0004399127625569986",
            "extra": "mean: 66.53196795320451 usec\nrounds: 5676"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20999.391469789603,
            "unit": "iter/sec",
            "range": "stddev: 0.0007370661949197322",
            "extra": "mean: 47.620427546133044 usec\nrounds: 3465"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 37561.4144993206,
            "unit": "iter/sec",
            "range": "stddev: 0.0003796126211410539",
            "extra": "mean: 26.623065540252423 usec\nrounds: 5352"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 40771.57362836632,
            "unit": "iter/sec",
            "range": "stddev: 0.0003085452988897707",
            "extra": "mean: 24.52689241565752 usec\nrounds: 11783"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21199.92855183455,
            "unit": "iter/sec",
            "range": "stddev: 0.00041310177912810586",
            "extra": "mean: 47.169970292822725 usec\nrounds: 8869"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 41724.35136051015,
            "unit": "iter/sec",
            "range": "stddev: 0.0002990057583732409",
            "extra": "mean: 23.966819552441173 usec\nrounds: 14886"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 22327.1871544778,
            "unit": "iter/sec",
            "range": "stddev: 0.0005474120944616186",
            "extra": "mean: 44.78844527441722 usec\nrounds: 5460"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18302.216787058285,
            "unit": "iter/sec",
            "range": "stddev: 0.0003369066003045591",
            "extra": "mean: 54.63819009657409 usec\nrounds: 8803"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 23713.8430083375,
            "unit": "iter/sec",
            "range": "stddev: 0.000008785857159724987",
            "extra": "mean: 42.16946193193622 usec\nrounds: 1957"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 30672.704217227834,
            "unit": "iter/sec",
            "range": "stddev: 0.0005207577693696732",
            "extra": "mean: 32.60227702513211 usec\nrounds: 4986"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21973.830132465766,
            "unit": "iter/sec",
            "range": "stddev: 0.00028642082979800555",
            "extra": "mean: 45.50867982375662 usec\nrounds: 7766"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21154.571987831656,
            "unit": "iter/sec",
            "range": "stddev: 0.0004971132563421116",
            "extra": "mean: 47.27110529937506 usec\nrounds: 5434"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 66461.26352360386,
            "unit": "iter/sec",
            "range": "stddev: 0.00037872001958707863",
            "extra": "mean: 15.0463585400366 usec\nrounds: 9410"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 69491.00494486213,
            "unit": "iter/sec",
            "range": "stddev: 0.00033760876070694295",
            "extra": "mean: 14.390351683551755 usec\nrounds: 9348"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 54526.67844438661,
            "unit": "iter/sec",
            "range": "stddev: 0.0004036472278028248",
            "extra": "mean: 18.339646362650345 usec\nrounds: 8117"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 64582.613788457515,
            "unit": "iter/sec",
            "range": "stddev: 0.00036429331286967414",
            "extra": "mean: 15.484043480735124 usec\nrounds: 8287"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 60569.22923246688,
            "unit": "iter/sec",
            "range": "stddev: 0.0003490888118700713",
            "extra": "mean: 16.510033438958978 usec\nrounds: 8011"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 60532.57966249385,
            "unit": "iter/sec",
            "range": "stddev: 0.00033395076697071926",
            "extra": "mean: 16.52002947132951 usec\nrounds: 7888"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 39433.63766229014,
            "unit": "iter/sec",
            "range": "stddev: 0.00035593686797884716",
            "extra": "mean: 25.359060418518947 usec\nrounds: 6039"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 34834.65229584855,
            "unit": "iter/sec",
            "range": "stddev: 0.00042785641101105397",
            "extra": "mean: 28.70704698031896 usec\nrounds: 3650"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 41227.83768515971,
            "unit": "iter/sec",
            "range": "stddev: 0.00030616488708821776",
            "extra": "mean: 24.255455928506237 usec\nrounds: 6934"
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
        "date": 1728995753609,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 48762.22807045429,
            "unit": "iter/sec",
            "range": "stddev: 0.000007561461618487112",
            "extra": "mean: 20.507676526904106 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2793.2560227825866,
            "unit": "iter/sec",
            "range": "stddev: 0.00011740719167592583",
            "extra": "mean: 358.00513516975064 usec\nrounds: 2211"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 318.3626667121428,
            "unit": "iter/sec",
            "range": "stddev: 0.0010234891386446613",
            "extra": "mean: 3.1410718170173513 msec\nrounds: 302"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.042872198029123,
            "unit": "iter/sec",
            "range": "stddev: 0.002086385611548698",
            "extra": "mean: 32.2135140595492 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14599.485075227964,
            "unit": "iter/sec",
            "range": "stddev: 0.00047372953377392647",
            "extra": "mean: 68.49556644273534 usec\nrounds: 5418"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22071.62341386105,
            "unit": "iter/sec",
            "range": "stddev: 0.0006071630676626913",
            "extra": "mean: 45.307043403612845 usec\nrounds: 6600"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 32995.75909008328,
            "unit": "iter/sec",
            "range": "stddev: 0.0005767484053589163",
            "extra": "mean: 30.30692511937224 usec\nrounds: 5269"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 43060.86693503772,
            "unit": "iter/sec",
            "range": "stddev: 0.00024769521132391077",
            "extra": "mean: 23.222941644640255 usec\nrounds: 10892"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 20606.40272476611,
            "unit": "iter/sec",
            "range": "stddev: 0.00040430766962721437",
            "extra": "mean: 48.52860605301745 usec\nrounds: 8604"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 40251.74233886758,
            "unit": "iter/sec",
            "range": "stddev: 0.0003546577267036678",
            "extra": "mean: 24.84364506712018 usec\nrounds: 14639"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 21600.555970784164,
            "unit": "iter/sec",
            "range": "stddev: 0.0006231005725918352",
            "extra": "mean: 46.295104688627006 usec\nrounds: 5178"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18590.82352880889,
            "unit": "iter/sec",
            "range": "stddev: 0.0003045941788016604",
            "extra": "mean: 53.78997861231755 usec\nrounds: 7940"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20166.041196253587,
            "unit": "iter/sec",
            "range": "stddev: 0.0004082538585831566",
            "extra": "mean: 49.58831484415386 usec\nrounds: 8818"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 35245.13583157587,
            "unit": "iter/sec",
            "range": "stddev: 0.00031309660882895867",
            "extra": "mean: 28.372709493265937 usec\nrounds: 12430"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20160.55373384904,
            "unit": "iter/sec",
            "range": "stddev: 0.0004301083308400705",
            "extra": "mean: 49.60181219234204 usec\nrounds: 8549"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 22413.230846277387,
            "unit": "iter/sec",
            "range": "stddev: 0.0004689008223723494",
            "extra": "mean: 44.61650383465756 usec\nrounds: 5348"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 57420.724437565565,
            "unit": "iter/sec",
            "range": "stddev: 0.00041370134355360965",
            "extra": "mean: 17.41531493715854 usec\nrounds: 8563"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 67474.75420362638,
            "unit": "iter/sec",
            "range": "stddev: 0.00036836395915285775",
            "extra": "mean: 14.820357803485793 usec\nrounds: 8890"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 61114.83843724415,
            "unit": "iter/sec",
            "range": "stddev: 0.0003763455783907592",
            "extra": "mean: 16.362638363625084 usec\nrounds: 8055"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 55081.6615533441,
            "unit": "iter/sec",
            "range": "stddev: 0.0004175277534367366",
            "extra": "mean: 18.15486264936916 usec\nrounds: 8224"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 57886.20158217643,
            "unit": "iter/sec",
            "range": "stddev: 0.0004010492931211934",
            "extra": "mean: 17.275274118312627 usec\nrounds: 8213"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 56022.75921387487,
            "unit": "iter/sec",
            "range": "stddev: 0.0004151431261658313",
            "extra": "mean: 17.849888403074853 usec\nrounds: 7436"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37265.542765906,
            "unit": "iter/sec",
            "range": "stddev: 0.0004453069400484266",
            "extra": "mean: 26.83444076695143 usec\nrounds: 5934"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37000.92578775476,
            "unit": "iter/sec",
            "range": "stddev: 0.0004075254220719319",
            "extra": "mean: 27.02635079284811 usec\nrounds: 6182"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38603.398922755,
            "unit": "iter/sec",
            "range": "stddev: 0.0003975599633236896",
            "extra": "mean: 25.904454734698092 usec\nrounds: 6698"
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
        "date": 1729244390954,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 46155.72030090105,
            "unit": "iter/sec",
            "range": "stddev: 0.000009432659707362432",
            "extra": "mean: 21.665786894468162 usec\nrounds: 13"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2984.9855068133206,
            "unit": "iter/sec",
            "range": "stddev: 0.00006769252073286464",
            "extra": "mean: 335.01000179648094 usec\nrounds: 1937"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 314.35884762974075,
            "unit": "iter/sec",
            "range": "stddev: 0.000642070292771545",
            "extra": "mean: 3.181077954509566 msec\nrounds: 310"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.76953374999749,
            "unit": "iter/sec",
            "range": "stddev: 0.0006506734591841413",
            "extra": "mean: 31.476697387794655 msec\nrounds: 30"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14540.726145789877,
            "unit": "iter/sec",
            "range": "stddev: 0.00049153081879251",
            "extra": "mean: 68.77235634408396 usec\nrounds: 5195"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22625.574878935302,
            "unit": "iter/sec",
            "range": "stddev: 0.0006149903139031515",
            "extra": "mean: 44.19777200582924 usec\nrounds: 4905"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 36066.833929097724,
            "unit": "iter/sec",
            "range": "stddev: 0.0004588237521698294",
            "extra": "mean: 27.726303949103436 usec\nrounds: 5917"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 40143.856486625984,
            "unit": "iter/sec",
            "range": "stddev: 0.0003127294267197575",
            "extra": "mean: 24.91041189162163 usec\nrounds: 11988"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21622.720948853155,
            "unit": "iter/sec",
            "range": "stddev: 0.00038998722496472367",
            "extra": "mean: 46.24764858989862 usec\nrounds: 9377"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39370.69914141755,
            "unit": "iter/sec",
            "range": "stddev: 0.0003490268154544468",
            "extra": "mean: 25.399599748230298 usec\nrounds: 16191"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23308.629114302385,
            "unit": "iter/sec",
            "range": "stddev: 0.0005006718141210994",
            "extra": "mean: 42.90256604522447 usec\nrounds: 8994"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18279.686155266707,
            "unit": "iter/sec",
            "range": "stddev: 0.0003717223593025959",
            "extra": "mean: 54.705534411589554 usec\nrounds: 9073"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20243.875293520552,
            "unit": "iter/sec",
            "range": "stddev: 0.00048731759011587774",
            "extra": "mean: 49.39765659987392 usec\nrounds: 5241"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34240.1077205308,
            "unit": "iter/sec",
            "range": "stddev: 0.0003199828380883718",
            "extra": "mean: 29.20551559481185 usec\nrounds: 13476"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21058.54337705678,
            "unit": "iter/sec",
            "range": "stddev: 0.0004457442761987343",
            "extra": "mean: 47.48666525005224 usec\nrounds: 8577"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20131.692533270172,
            "unit": "iter/sec",
            "range": "stddev: 0.0005554188445038946",
            "extra": "mean: 49.672922351032994 usec\nrounds: 4851"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 63361.06855053608,
            "unit": "iter/sec",
            "range": "stddev: 0.0003938848098322161",
            "extra": "mean: 15.78256211386983 usec\nrounds: 8624"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 62658.45757759703,
            "unit": "iter/sec",
            "range": "stddev: 0.000397398852316803",
            "extra": "mean: 15.959537445708543 usec\nrounds: 6863"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 50750.190341413814,
            "unit": "iter/sec",
            "range": "stddev: 0.0004909847465755803",
            "extra": "mean: 19.704359594962295 usec\nrounds: 4491"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 65184.713459913815,
            "unit": "iter/sec",
            "range": "stddev: 0.00032367349355846506",
            "extra": "mean: 15.341020109185 usec\nrounds: 8494"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 55212.12658951029,
            "unit": "iter/sec",
            "range": "stddev: 0.0004682688761073555",
            "extra": "mean: 18.11196310974896 usec\nrounds: 7655"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 58068.31423333168,
            "unit": "iter/sec",
            "range": "stddev: 0.00036611348915576163",
            "extra": "mean: 17.2210957594149 usec\nrounds: 7798"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37225.49834741861,
            "unit": "iter/sec",
            "range": "stddev: 0.0004314166737087937",
            "extra": "mean: 26.863307259641957 usec\nrounds: 5317"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 35756.958051545545,
            "unit": "iter/sec",
            "range": "stddev: 0.000409576671779109",
            "extra": "mean: 27.966584812904024 usec\nrounds: 6247"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 34609.994695901776,
            "unit": "iter/sec",
            "range": "stddev: 0.000462200908058175",
            "extra": "mean: 28.893387843206217 usec\nrounds: 3978"
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
        "date": 1729247464587,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 26538.9095402961,
            "unit": "iter/sec",
            "range": "stddev: 0.000011854227615819644",
            "extra": "mean: 37.68052332676374 usec\nrounds: 13"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2523.0336349542463,
            "unit": "iter/sec",
            "range": "stddev: 0.00014426345929625145",
            "extra": "mean: 396.3482635133932 usec\nrounds: 1121"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 324.20992917298986,
            "unit": "iter/sec",
            "range": "stddev: 0.00015226277023094805",
            "extra": "mean: 3.084421265415429 msec\nrounds: 303"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 32.00808252344194,
            "unit": "iter/sec",
            "range": "stddev: 0.0004908310716629725",
            "extra": "mean: 31.242108903825283 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14863.275013499631,
            "unit": "iter/sec",
            "range": "stddev: 0.00046745252071072436",
            "extra": "mean: 67.27992310522046 usec\nrounds: 5532"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 22043.971303322585,
            "unit": "iter/sec",
            "range": "stddev: 0.0006275564953011926",
            "extra": "mean: 45.36387687318731 usec\nrounds: 6714"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 34229.743182918675,
            "unit": "iter/sec",
            "range": "stddev: 0.0005576999387578525",
            "extra": "mean: 29.214358829867585 usec\nrounds: 5569"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 39182.638254283855,
            "unit": "iter/sec",
            "range": "stddev: 0.0003504163178786339",
            "extra": "mean: 25.521507600133834 usec\nrounds: 11905"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21636.56065614204,
            "unit": "iter/sec",
            "range": "stddev: 0.0004298166699669442",
            "extra": "mean: 46.21806653527102 usec\nrounds: 10326"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 40665.94882321344,
            "unit": "iter/sec",
            "range": "stddev: 0.00034840618372324045",
            "extra": "mean: 24.590598004912838 usec\nrounds: 12208"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 22952.652775853305,
            "unit": "iter/sec",
            "range": "stddev: 0.000467700202495641",
            "extra": "mean: 43.56794875806347 usec\nrounds: 9184"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18643.488652439657,
            "unit": "iter/sec",
            "range": "stddev: 0.00040293142975552976",
            "extra": "mean: 53.63802980453133 usec\nrounds: 8016"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22002.550933644976,
            "unit": "iter/sec",
            "range": "stddev: 0.0003408939336143945",
            "extra": "mean: 45.44927554154006 usec\nrounds: 9048"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34414.14191337894,
            "unit": "iter/sec",
            "range": "stddev: 0.00032985268696268807",
            "extra": "mean: 29.057821709372252 usec\nrounds: 13058"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20333.19481109717,
            "unit": "iter/sec",
            "range": "stddev: 0.00047094297032887846",
            "extra": "mean: 49.18066291551162 usec\nrounds: 8509"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 22492.353368145494,
            "unit": "iter/sec",
            "range": "stddev: 0.000506822420754941",
            "extra": "mean: 44.45955403742844 usec\nrounds: 4731"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 66827.47013207249,
            "unit": "iter/sec",
            "range": "stddev: 0.000353728773821818",
            "extra": "mean: 14.96390628021201 usec\nrounds: 9029"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 61071.28910896697,
            "unit": "iter/sec",
            "range": "stddev: 0.00037403860819132075",
            "extra": "mean: 16.374306398146295 usec\nrounds: 9079"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 57972.24924833093,
            "unit": "iter/sec",
            "range": "stddev: 0.0004484754069160647",
            "extra": "mean: 17.24963259086917 usec\nrounds: 7367"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 65023.631102584804,
            "unit": "iter/sec",
            "range": "stddev: 0.00035781040316019134",
            "extra": "mean: 15.379024256925085 usec\nrounds: 8478"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 58295.02624840362,
            "unit": "iter/sec",
            "range": "stddev: 0.00038931905550922016",
            "extra": "mean: 17.15412213280176 usec\nrounds: 7196"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 52452.49516022242,
            "unit": "iter/sec",
            "range": "stddev: 0.0004375403855921574",
            "extra": "mean: 19.06486997320872 usec\nrounds: 4596"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 39596.35951492325,
            "unit": "iter/sec",
            "range": "stddev: 0.00037338989836523036",
            "extra": "mean: 25.25484696700755 usec\nrounds: 5937"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 38103.042667933165,
            "unit": "iter/sec",
            "range": "stddev: 0.0003862721370424975",
            "extra": "mean: 26.24462326315956 usec\nrounds: 6336"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38986.136010794056,
            "unit": "iter/sec",
            "range": "stddev: 0.00039457734756861453",
            "extra": "mean: 25.650143931245992 usec\nrounds: 6582"
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
        "date": 1729852961399,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 26429.687783067497,
            "unit": "iter/sec",
            "range": "stddev: 0.000011625781575180323",
            "extra": "mean: 37.836239618413586 usec\nrounds: 17"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2959.087657925755,
            "unit": "iter/sec",
            "range": "stddev: 0.00007076075843896867",
            "extra": "mean: 337.9419995624511 usec\nrounds: 1159"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 321.7354728880623,
            "unit": "iter/sec",
            "range": "stddev: 0.00035432920542221766",
            "extra": "mean: 3.108143441640078 msec\nrounds: 314"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 32.346213581631766,
            "unit": "iter/sec",
            "range": "stddev: 0.0004047837003452945",
            "extra": "mean: 30.915519600966945 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14717.872450564799,
            "unit": "iter/sec",
            "range": "stddev: 0.0004668868534044814",
            "extra": "mean: 67.94460295527463 usec\nrounds: 5618"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21529.489371424792,
            "unit": "iter/sec",
            "range": "stddev: 0.0006424389910236254",
            "extra": "mean: 46.44792000163548 usec\nrounds: 6322"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 45600.16338859773,
            "unit": "iter/sec",
            "range": "stddev: 0.000009128351282419443",
            "extra": "mean: 21.929745985297256 usec\nrounds: 4173"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 35759.70281076886,
            "unit": "iter/sec",
            "range": "stddev: 0.0005538235528749057",
            "extra": "mean: 27.964438219516044 usec\nrounds: 6260"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21707.398680938524,
            "unit": "iter/sec",
            "range": "stddev: 0.0003114448509388016",
            "extra": "mean: 46.06724254242907 usec\nrounds: 6587"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39279.44003715134,
            "unit": "iter/sec",
            "range": "stddev: 0.0003460069320335769",
            "extra": "mean: 25.458611402152844 usec\nrounds: 14820"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 21808.025604164155,
            "unit": "iter/sec",
            "range": "stddev: 0.000600069455395611",
            "extra": "mean: 45.85467837166579 usec\nrounds: 5419"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18596.288147859632,
            "unit": "iter/sec",
            "range": "stddev: 0.0003180071273408156",
            "extra": "mean: 53.77417213849187 usec\nrounds: 7866"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20339.790527350564,
            "unit": "iter/sec",
            "range": "stddev: 0.00046835382986616225",
            "extra": "mean: 49.164714781861555 usec\nrounds: 5054"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 33875.01435016585,
            "unit": "iter/sec",
            "range": "stddev: 0.00031836791338533244",
            "extra": "mean: 29.52028269753645 usec\nrounds: 12245"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20754.591620369,
            "unit": "iter/sec",
            "range": "stddev: 0.00042254197739172",
            "extra": "mean: 48.18210920703343 usec\nrounds: 9052"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 21015.551545168615,
            "unit": "iter/sec",
            "range": "stddev: 0.0005433290829862076",
            "extra": "mean: 47.5838094399143 usec\nrounds: 4195"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 64894.19666603504,
            "unit": "iter/sec",
            "range": "stddev: 0.00035395041899658554",
            "extra": "mean: 15.409698422592385 usec\nrounds: 7243"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 57748.3861470103,
            "unit": "iter/sec",
            "range": "stddev: 0.0004022911354212574",
            "extra": "mean: 17.31650123441192 usec\nrounds: 8237"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 56898.68784274927,
            "unit": "iter/sec",
            "range": "stddev: 0.0004363274574920079",
            "extra": "mean: 17.57509773799524 usec\nrounds: 6902"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 62691.56120524876,
            "unit": "iter/sec",
            "range": "stddev: 0.0003671197498697547",
            "extra": "mean: 15.951110177748713 usec\nrounds: 8112"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 56301.26078879795,
            "unit": "iter/sec",
            "range": "stddev: 0.00041059566119767114",
            "extra": "mean: 17.761591587642855 usec\nrounds: 7299"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 55999.623379986944,
            "unit": "iter/sec",
            "range": "stddev: 0.0004082372608214114",
            "extra": "mean: 17.85726295361798 usec\nrounds: 6704"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38211.68403378527,
            "unit": "iter/sec",
            "range": "stddev: 0.00041913088185766836",
            "extra": "mean: 26.170005988635292 usec\nrounds: 5887"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37100.46917357266,
            "unit": "iter/sec",
            "range": "stddev: 0.0003905451906617059",
            "extra": "mean: 26.953837034285225 usec\nrounds: 6511"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37641.62557628487,
            "unit": "iter/sec",
            "range": "stddev: 0.00043396519653513937",
            "extra": "mean: 26.56633407006801 usec\nrounds: 5763"
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
        "date": 1729853341201,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 50266.010464014624,
            "unit": "iter/sec",
            "range": "stddev: 0.000007283466464693586",
            "extra": "mean: 19.894158911137353 usec\nrounds: 21"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 3091.1573916484076,
            "unit": "iter/sec",
            "range": "stddev: 0.000031232072561596965",
            "extra": "mean: 323.5034238961008 usec\nrounds: 2250"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 314.9054096723614,
            "unit": "iter/sec",
            "range": "stddev: 0.0011138733331901732",
            "extra": "mean: 3.1755567522337422 msec\nrounds: 312"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 32.04720058072507,
            "unit": "iter/sec",
            "range": "stddev: 0.0014532931402046435",
            "extra": "mean: 31.203973572701216 msec\nrounds: 28"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14739.286115770787,
            "unit": "iter/sec",
            "range": "stddev: 0.0004930934198992351",
            "extra": "mean: 67.84589105235001 usec\nrounds: 5584"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 21659.90293773984,
            "unit": "iter/sec",
            "range": "stddev: 0.0006420993156212276",
            "extra": "mean: 46.168258596284716 usec\nrounds: 5610"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 46227.04038297045,
            "unit": "iter/sec",
            "range": "stddev: 0.000009030418428837567",
            "extra": "mean: 21.632360447812474 usec\nrounds: 4069"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 38078.994147654266,
            "unit": "iter/sec",
            "range": "stddev: 0.0004304403992664099",
            "extra": "mean: 26.26119786994431 usec\nrounds: 11933"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 20666.766611097308,
            "unit": "iter/sec",
            "range": "stddev: 0.0004355419011244787",
            "extra": "mean: 48.38686277431691 usec\nrounds: 8787"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 42365.13368799908,
            "unit": "iter/sec",
            "range": "stddev: 0.0003222834283909943",
            "extra": "mean: 23.604315930278148 usec\nrounds: 12713"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23092.799038363544,
            "unit": "iter/sec",
            "range": "stddev: 0.0004266437352982215",
            "extra": "mean: 43.30354230072858 usec\nrounds: 9071"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18722.19022109573,
            "unit": "iter/sec",
            "range": "stddev: 0.0003421911794101574",
            "extra": "mean: 53.41255420389988 usec\nrounds: 8876"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20998.93411474349,
            "unit": "iter/sec",
            "range": "stddev: 0.00038011895526206296",
            "extra": "mean: 47.62146471510158 usec\nrounds: 8915"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 34031.39862683824,
            "unit": "iter/sec",
            "range": "stddev: 0.0003473831771882955",
            "extra": "mean: 29.384628324131477 usec\nrounds: 12686"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 19774.333934193084,
            "unit": "iter/sec",
            "range": "stddev: 0.0005368576622506646",
            "extra": "mean: 50.57060345637407 usec\nrounds: 5035"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 23649.884824307253,
            "unit": "iter/sec",
            "range": "stddev: 0.00036783252569734304",
            "extra": "mean: 42.283504018260764 usec\nrounds: 5290"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 65282.046928214484,
            "unit": "iter/sec",
            "range": "stddev: 0.0003739384774112141",
            "extra": "mean: 15.318147133156243 usec\nrounds: 8064"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 62729.423776454794,
            "unit": "iter/sec",
            "range": "stddev: 0.0003422158567211962",
            "extra": "mean: 15.941482318786187 usec\nrounds: 9476"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 60738.19517878913,
            "unit": "iter/sec",
            "range": "stddev: 0.000395478974062867",
            "extra": "mean: 16.46410462241094 usec\nrounds: 8714"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 65167.24046091432,
            "unit": "iter/sec",
            "range": "stddev: 0.00034566713798638054",
            "extra": "mean: 15.345133427888126 usec\nrounds: 8584"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 53659.68645526958,
            "unit": "iter/sec",
            "range": "stddev: 0.0003987494195679223",
            "extra": "mean: 18.63596427894886 usec\nrounds: 8083"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 58511.26223663237,
            "unit": "iter/sec",
            "range": "stddev: 0.00038776412011114935",
            "extra": "mean: 17.090726840856394 usec\nrounds: 7940"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 49051.29008280167,
            "unit": "iter/sec",
            "range": "stddev: 0.00000805283629935979",
            "extra": "mean: 20.386823635258867 usec\nrounds: 3526"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36868.72384743586,
            "unit": "iter/sec",
            "range": "stddev: 0.00045621833144649535",
            "extra": "mean: 27.123260467002787 usec\nrounds: 6240"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 39923.47951100817,
            "unit": "iter/sec",
            "range": "stddev: 0.0003417074620263428",
            "extra": "mean: 25.047916971371908 usec\nrounds: 5832"
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
        "date": 1732013580985,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47396.61275513808,
            "unit": "iter/sec",
            "range": "stddev: 0.00000848292985457534",
            "extra": "mean: 21.098554134368896 usec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2833.2712704118417,
            "unit": "iter/sec",
            "range": "stddev: 0.0003199409483996426",
            "extra": "mean: 352.94890766129885 usec\nrounds: 2056"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 305.96000196298803,
            "unit": "iter/sec",
            "range": "stddev: 0.0006419122762391998",
            "extra": "mean: 3.268401077213256 msec\nrounds: 304"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 31.303521816237314,
            "unit": "iter/sec",
            "range": "stddev: 0.0018976224777342602",
            "extra": "mean: 31.94528736639768 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14411.219942121694,
            "unit": "iter/sec",
            "range": "stddev: 0.000515814250634228",
            "extra": "mean: 69.39037805378014 usec\nrounds: 5366"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20991.075684281488,
            "unit": "iter/sec",
            "range": "stddev: 0.0006820717160162282",
            "extra": "mean: 47.639292766154846 usec\nrounds: 5772"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 34516.78750191951,
            "unit": "iter/sec",
            "range": "stddev: 0.0005118029866650776",
            "extra": "mean: 28.97140992464577 usec\nrounds: 5985"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 38749.71068159472,
            "unit": "iter/sec",
            "range": "stddev: 0.0003604851208288353",
            "extra": "mean: 25.806644292572187 usec\nrounds: 12085"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21077.057088940033,
            "unit": "iter/sec",
            "range": "stddev: 0.0004740065200190278",
            "extra": "mean: 47.444953808316036 usec\nrounds: 9833"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39328.49468239168,
            "unit": "iter/sec",
            "range": "stddev: 0.0003488583181267546",
            "extra": "mean: 25.426856737736376 usec\nrounds: 13680"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 21847.849998018937,
            "unit": "iter/sec",
            "range": "stddev: 0.0005072639995749047",
            "extra": "mean: 45.77109418504225 usec\nrounds: 8984"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 18131.824710561326,
            "unit": "iter/sec",
            "range": "stddev: 0.00040842970937112947",
            "extra": "mean: 55.15164722596979 usec\nrounds: 8650"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20661.630198270577,
            "unit": "iter/sec",
            "range": "stddev: 0.0004366986124072208",
            "extra": "mean: 48.398891588123675 usec\nrounds: 6941"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 32964.50093850631,
            "unit": "iter/sec",
            "range": "stddev: 0.0003364608188949466",
            "extra": "mean: 30.335663259864052 usec\nrounds: 12497"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 20758.32480805012,
            "unit": "iter/sec",
            "range": "stddev: 0.00044250380973637443",
            "extra": "mean: 48.17344411203152 usec\nrounds: 8278"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20643.177798291603,
            "unit": "iter/sec",
            "range": "stddev: 0.0005255016738182991",
            "extra": "mean: 48.442154099101856 usec\nrounds: 5124"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 61048.68452877518,
            "unit": "iter/sec",
            "range": "stddev: 0.00042775624404922056",
            "extra": "mean: 16.380369335045245 usec\nrounds: 7537"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 65588.33275874169,
            "unit": "iter/sec",
            "range": "stddev: 0.0003611633688779202",
            "extra": "mean: 15.24661411471416 usec\nrounds: 7780"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 60762.61124467523,
            "unit": "iter/sec",
            "range": "stddev: 0.00035494237939084244",
            "extra": "mean: 16.45748889844875 usec\nrounds: 7297"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 53803.651191255405,
            "unit": "iter/sec",
            "range": "stddev: 0.0004256713039105653",
            "extra": "mean: 18.586099230427838 usec\nrounds: 8115"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 54230.87382326046,
            "unit": "iter/sec",
            "range": "stddev: 0.0004588249868974674",
            "extra": "mean: 18.439680748258287 usec\nrounds: 7771"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 54867.545130433224,
            "unit": "iter/sec",
            "range": "stddev: 0.0004010600181095515",
            "extra": "mean: 18.22571062041799 usec\nrounds: 6748"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36277.08120502897,
            "unit": "iter/sec",
            "range": "stddev: 0.0004608786347655934",
            "extra": "mean: 27.56561351637555 usec\nrounds: 5265"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 36434.782051306414,
            "unit": "iter/sec",
            "range": "stddev: 0.0004047613771712436",
            "extra": "mean: 27.44630113587145 usec\nrounds: 6428"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37023.323965526666,
            "unit": "iter/sec",
            "range": "stddev: 0.00044424752039060966",
            "extra": "mean: 27.01000053185729 usec\nrounds: 6367"
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
        "date": 1733403041783,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 41774.48323172119,
            "unit": "iter/sec",
            "range": "stddev: 0.0002591896616884309",
            "extra": "mean: 23.93805793965289 usec\nrounds: 2881"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2894.259128454213,
            "unit": "iter/sec",
            "range": "stddev: 0.00007316214097836265",
            "extra": "mean: 345.5115646587205 usec\nrounds: 2187"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 311.652341143896,
            "unit": "iter/sec",
            "range": "stddev: 0.0005175236714849614",
            "extra": "mean: 3.2087036353700302 msec\nrounds: 289"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 29.65845792115986,
            "unit": "iter/sec",
            "range": "stddev: 0.002561645383156541",
            "extra": "mean: 33.717194692261764 msec\nrounds: 31"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14539.20345000094,
            "unit": "iter/sec",
            "range": "stddev: 0.00044875001243950715",
            "extra": "mean: 68.7795588966695 usec\nrounds: 4783"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20170.201954317785,
            "unit": "iter/sec",
            "range": "stddev: 0.0007036012327412733",
            "extra": "mean: 49.57808564658087 usec\nrounds: 5116"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 31492.08319030313,
            "unit": "iter/sec",
            "range": "stddev: 0.0006499834443772247",
            "extra": "mean: 31.754012395976222 usec\nrounds: 4969"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 40310.49305155057,
            "unit": "iter/sec",
            "range": "stddev: 0.0002919545219102813",
            "extra": "mean: 24.80743658285604 usec\nrounds: 10992"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 19148.924181350176,
            "unit": "iter/sec",
            "range": "stddev: 0.0005655886582706505",
            "extra": "mean: 52.222254917795105 usec\nrounds: 4260"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39622.58004200596,
            "unit": "iter/sec",
            "range": "stddev: 0.0003106618067215941",
            "extra": "mean: 25.238134390538118 usec\nrounds: 13279"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 21732.925987915514,
            "unit": "iter/sec",
            "range": "stddev: 0.0005114208461122247",
            "extra": "mean: 46.013132357605464 usec\nrounds: 8822"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 17742.75069581285,
            "unit": "iter/sec",
            "range": "stddev: 0.000430344536383214",
            "extra": "mean: 56.361046668823015 usec\nrounds: 8458"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 20317.432655506225,
            "unit": "iter/sec",
            "range": "stddev: 0.0004551923573946105",
            "extra": "mean: 49.21881701076981 usec\nrounds: 6972"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 30829.357728212995,
            "unit": "iter/sec",
            "range": "stddev: 0.00042979538806353255",
            "extra": "mean: 32.43661476232656 usec\nrounds: 10922"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 22605.69497091255,
            "unit": "iter/sec",
            "range": "stddev: 0.000010766024980167828",
            "extra": "mean: 44.2366404256419 usec\nrounds: 4416"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 18687.683796448524,
            "unit": "iter/sec",
            "range": "stddev: 0.0007205704089859737",
            "extra": "mean: 53.51117938917843 usec\nrounds: 5001"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 59903.59606211758,
            "unit": "iter/sec",
            "range": "stddev: 0.0004553403072059124",
            "extra": "mean: 16.69348863402192 usec\nrounds: 7993"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 59503.25450766259,
            "unit": "iter/sec",
            "range": "stddev: 0.00043429005542840025",
            "extra": "mean: 16.805803451830084 usec\nrounds: 6826"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 55827.91125029082,
            "unit": "iter/sec",
            "range": "stddev: 0.0004212495375839823",
            "extra": "mean: 17.91218724835941 usec\nrounds: 7383"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 63046.48793618781,
            "unit": "iter/sec",
            "range": "stddev: 0.0003496730372882308",
            "extra": "mean: 15.8613117516101 usec\nrounds: 7924"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 46585.0808444031,
            "unit": "iter/sec",
            "range": "stddev: 0.00048350175042666016",
            "extra": "mean: 21.4660999159808 usec\nrounds: 6717"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 54298.705185177394,
            "unit": "iter/sec",
            "range": "stddev: 0.0004603726720520483",
            "extra": "mean: 18.416645417043622 usec\nrounds: 7076"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 47081.33062628126,
            "unit": "iter/sec",
            "range": "stddev: 0.000009226031255650504",
            "extra": "mean: 21.239841497635798 usec\nrounds: 5690"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 32110.579928411276,
            "unit": "iter/sec",
            "range": "stddev: 0.0005837886862379871",
            "extra": "mean: 31.14238367010012 usec\nrounds: 5701"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 34120.56601570631,
            "unit": "iter/sec",
            "range": "stddev: 0.00048724125801212693",
            "extra": "mean: 29.307837377014266 usec\nrounds: 3999"
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
        "date": 1734540966560,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 23097.65526323083,
            "unit": "iter/sec",
            "range": "stddev: 0.00039920155399823684",
            "extra": "mean: 43.2944378381082 usec\nrounds: 2302"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 3083.5236090037147,
            "unit": "iter/sec",
            "range": "stddev: 0.00003620160675239771",
            "extra": "mean: 324.3043111718219 usec\nrounds: 1150"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 313.7471973005409,
            "unit": "iter/sec",
            "range": "stddev: 0.0006692957597418873",
            "extra": "mean: 3.1872794676858645 msec\nrounds: 312"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 29.999796013803504,
            "unit": "iter/sec",
            "range": "stddev: 0.005619935961245654",
            "extra": "mean: 33.33355998620391 msec\nrounds: 32"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15056.537506355735,
            "unit": "iter/sec",
            "range": "stddev: 0.0004470667714181034",
            "extra": "mean: 66.41633241227443 usec\nrounds: 4596"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20887.12681516496,
            "unit": "iter/sec",
            "range": "stddev: 0.0006824453303518939",
            "extra": "mean: 47.876379018006276 usec\nrounds: 5569"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 33168.90237727857,
            "unit": "iter/sec",
            "range": "stddev: 0.0005903862348264553",
            "extra": "mean: 30.14872149296752 usec\nrounds: 5388"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 41518.18101724121,
            "unit": "iter/sec",
            "range": "stddev: 0.0002852340207444226",
            "extra": "mean: 24.08583361551247 usec\nrounds: 11366"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 20772.930459339976,
            "unit": "iter/sec",
            "range": "stddev: 0.0004876542634020034",
            "extra": "mean: 48.13957289065961 usec\nrounds: 7280"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 39691.146049267656,
            "unit": "iter/sec",
            "range": "stddev: 0.00034184866268600775",
            "extra": "mean: 25.19453579795162 usec\nrounds: 12661"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 22053.31536402691,
            "unit": "iter/sec",
            "range": "stddev: 0.0005273936302524611",
            "extra": "mean: 45.344656052540174 usec\nrounds: 8909"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 17369.318632395978,
            "unit": "iter/sec",
            "range": "stddev: 0.0005457118023792606",
            "extra": "mean: 57.572782281446166 usec\nrounds: 4930"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 23115.721360762724,
            "unit": "iter/sec",
            "range": "stddev: 0.000011726252569900618",
            "extra": "mean: 43.260601059910165 usec\nrounds: 4398"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 33376.18665902767,
            "unit": "iter/sec",
            "range": "stddev: 0.00037866801098105805",
            "extra": "mean: 29.961481526216165 usec\nrounds: 12978"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 19022.77875431441,
            "unit": "iter/sec",
            "range": "stddev: 0.0006446937446736833",
            "extra": "mean: 52.568555462655404 usec\nrounds: 4768"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 20822.919828535294,
            "unit": "iter/sec",
            "range": "stddev: 0.0005159120453582389",
            "extra": "mean: 48.024004713768385 usec\nrounds: 5039"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 61268.90610619863,
            "unit": "iter/sec",
            "range": "stddev: 0.000443485880214751",
            "extra": "mean: 16.321492638805726 usec\nrounds: 8430"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 60527.40702950633,
            "unit": "iter/sec",
            "range": "stddev: 0.0004506366481778904",
            "extra": "mean: 16.521441262344396 usec\nrounds: 7334"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 57884.8737718197,
            "unit": "iter/sec",
            "range": "stddev: 0.00042042270991943676",
            "extra": "mean: 17.27567039261358 usec\nrounds: 7725"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 60098.014244460464,
            "unit": "iter/sec",
            "range": "stddev: 0.00039038915912523403",
            "extra": "mean: 16.639484891003285 usec\nrounds: 7967"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 49566.28943197796,
            "unit": "iter/sec",
            "range": "stddev: 0.00048483651289221057",
            "extra": "mean: 20.175002233571366 usec\nrounds: 5236"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 57526.48255450748,
            "unit": "iter/sec",
            "range": "stddev: 0.0003709892965556018",
            "extra": "mean: 17.383298188838165 usec\nrounds: 7332"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 25460.458667770195,
            "unit": "iter/sec",
            "range": "stddev: 0.0007862425740194534",
            "extra": "mean: 39.27659014508945 usec\nrounds: 1807"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 38046.439890276946,
            "unit": "iter/sec",
            "range": "stddev: 0.0003457421715271723",
            "extra": "mean: 26.283668140407467 usec\nrounds: 6100"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37165.433463691974,
            "unit": "iter/sec",
            "range": "stddev: 0.0004695687090938663",
            "extra": "mean: 26.906722370853817 usec\nrounds: 6441"
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
        "date": 1738866469477,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 34823.52063195971,
            "unit": "iter/sec",
            "range": "stddev: 0.00020066911475501945",
            "extra": "mean: 28.71622345623026 usec\nrounds: 3940"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2826.9485830535214,
            "unit": "iter/sec",
            "range": "stddev: 0.00010485425743376018",
            "extra": "mean: 353.7383049676314 usec\nrounds: 2376"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 319.7160999135377,
            "unit": "iter/sec",
            "range": "stddev: 0.0013619171484671917",
            "extra": "mean: 3.1277749236601933 msec\nrounds: 314"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 32.939519177107165,
            "unit": "iter/sec",
            "range": "stddev: 0.0005627424997527314",
            "extra": "mean: 30.358670222939864 msec\nrounds: 33"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15763.469143621913,
            "unit": "iter/sec",
            "range": "stddev: 0.00034876014944345185",
            "extra": "mean: 63.43781250744618 usec\nrounds: 5684"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 24366.893235552798,
            "unit": "iter/sec",
            "range": "stddev: 0.0004232386160197297",
            "extra": "mean: 41.03929008647432 usec\nrounds: 6566"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 39652.98224221751,
            "unit": "iter/sec",
            "range": "stddev: 0.00034031778361866966",
            "extra": "mean: 25.218784148227964 usec\nrounds: 6674"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 44331.40291743324,
            "unit": "iter/sec",
            "range": "stddev: 0.00018768771128181477",
            "extra": "mean: 22.557373198012463 usec\nrounds: 15491"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 22090.068382751564,
            "unit": "iter/sec",
            "range": "stddev: 0.0003286551648750753",
            "extra": "mean: 45.26921251094103 usec\nrounds: 10557"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 43182.955077589606,
            "unit": "iter/sec",
            "range": "stddev: 0.000249301650635633",
            "extra": "mean: 23.157285049233785 usec\nrounds: 17574"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23250.936952492077,
            "unit": "iter/sec",
            "range": "stddev: 0.0004597613033108271",
            "extra": "mean: 43.009019466323835 usec\nrounds: 5674"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19710.879185730453,
            "unit": "iter/sec",
            "range": "stddev: 0.0001967484462507343",
            "extra": "mean: 50.73340415601262 usec\nrounds: 9953"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22159.030693343462,
            "unit": "iter/sec",
            "range": "stddev: 0.00027358851410919636",
            "extra": "mean: 45.128327761213775 usec\nrounds: 10083"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 36365.022820379425,
            "unit": "iter/sec",
            "range": "stddev: 0.0002328992085989719",
            "extra": "mean: 27.498951532063586 usec\nrounds: 15548"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21828.711514301547,
            "unit": "iter/sec",
            "range": "stddev: 0.00031736017995078066",
            "extra": "mean: 45.8112243292431 usec\nrounds: 10852"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 23044.83843130028,
            "unit": "iter/sec",
            "range": "stddev: 0.0003530479572814663",
            "extra": "mean: 43.39366504916634 usec\nrounds: 6340"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 65958.01415969367,
            "unit": "iter/sec",
            "range": "stddev: 0.00029799885505102396",
            "extra": "mean: 15.161159909679188 usec\nrounds: 9837"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 75833.3561068685,
            "unit": "iter/sec",
            "range": "stddev: 0.0002512614620933709",
            "extra": "mean: 13.186809226677843 usec\nrounds: 9821"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 60292.387684059024,
            "unit": "iter/sec",
            "range": "stddev: 0.00033852794501852576",
            "extra": "mean: 16.585841735778438 usec\nrounds: 5327"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 68181.6624835488,
            "unit": "iter/sec",
            "range": "stddev: 0.0002533698536301684",
            "extra": "mean: 14.666700159170876 usec\nrounds: 5654"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 67531.4867371251,
            "unit": "iter/sec",
            "range": "stddev: 0.00020543184282180904",
            "extra": "mean: 14.807907367605086 usec\nrounds: 8810"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 65614.39601489823,
            "unit": "iter/sec",
            "range": "stddev: 0.000249477455245589",
            "extra": "mean: 15.240557876551096 usec\nrounds: 8520"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 43236.26666789106,
            "unit": "iter/sec",
            "range": "stddev: 0.0002637679591485104",
            "extra": "mean: 23.12873143468326 usec\nrounds: 6595"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 42303.036135782786,
            "unit": "iter/sec",
            "range": "stddev: 0.00021969214151750823",
            "extra": "mean: 23.638965222028876 usec\nrounds: 7457"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 40503.248924424326,
            "unit": "iter/sec",
            "range": "stddev: 0.0002700654765516291",
            "extra": "mean: 24.689377434040324 usec\nrounds: 7576"
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
        "date": 1738867986416,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47532.81732201836,
            "unit": "iter/sec",
            "range": "stddev: 0.00019672210391166357",
            "extra": "mean: 21.038096547598826 usec\nrounds: 3788"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2681.7111679349805,
            "unit": "iter/sec",
            "range": "stddev: 0.00012879502514592865",
            "extra": "mean: 372.8962357903883 usec\nrounds: 2356"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 322.85758060630474,
            "unit": "iter/sec",
            "range": "stddev: 0.000625706714685255",
            "extra": "mean: 3.0973409331819544 msec\nrounds: 318"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 33.36882459919982,
            "unit": "iter/sec",
            "range": "stddev: 0.0005732865902682899",
            "extra": "mean: 29.968091834555654 msec\nrounds: 34"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15866.884287310584,
            "unit": "iter/sec",
            "range": "stddev: 0.00032688087939847975",
            "extra": "mean: 63.02434566815 usec\nrounds: 5720"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 24529.7474597877,
            "unit": "iter/sec",
            "range": "stddev: 0.00041045418375023615",
            "extra": "mean: 40.7668281803279 usec\nrounds: 6770"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 36014.93223103947,
            "unit": "iter/sec",
            "range": "stddev: 0.000434751218049381",
            "extra": "mean: 27.766260771640436 usec\nrounds: 4254"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 41037.99144301396,
            "unit": "iter/sec",
            "range": "stddev: 0.0002551511293101794",
            "extra": "mean: 24.367664323645485 usec\nrounds: 5452"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 23395.530559738247,
            "unit": "iter/sec",
            "range": "stddev: 0.00019182973461189155",
            "extra": "mean: 42.74320676107754 usec\nrounds: 11061"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 43124.95087764244,
            "unit": "iter/sec",
            "range": "stddev: 0.0002486528964863043",
            "extra": "mean: 23.18843221032947 usec\nrounds: 17443"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 23772.3450826954,
            "unit": "iter/sec",
            "range": "stddev: 0.0003893953557350842",
            "extra": "mean: 42.06568584299788 usec\nrounds: 9262"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19638.531351557584,
            "unit": "iter/sec",
            "range": "stddev: 0.00024225860409401705",
            "extra": "mean: 50.920304685649896 usec\nrounds: 10363"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22030.532299525472,
            "unit": "iter/sec",
            "range": "stddev: 0.0002888288156258476",
            "extra": "mean: 45.39154961868713 usec\nrounds: 10754"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 35173.324846133655,
            "unit": "iter/sec",
            "range": "stddev: 0.00030104179547273867",
            "extra": "mean: 28.43063612480532 usec\nrounds: 7456"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 22304.13081242127,
            "unit": "iter/sec",
            "range": "stddev: 0.0002555054562477012",
            "extra": "mean: 44.83474421890924 usec\nrounds: 7738"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 23583.174400841497,
            "unit": "iter/sec",
            "range": "stddev: 0.00031610410907276763",
            "extra": "mean: 42.40311261762615 usec\nrounds: 6202"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 68739.23091673823,
            "unit": "iter/sec",
            "range": "stddev: 0.0003080726411774851",
            "extra": "mean: 14.547733320020267 usec\nrounds: 7106"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 68221.33455084501,
            "unit": "iter/sec",
            "range": "stddev: 0.0002688548016043082",
            "extra": "mean: 14.658171180376208 usec\nrounds: 4953"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 73750.50292129078,
            "unit": "iter/sec",
            "range": "stddev: 0.0001804799740261605",
            "extra": "mean: 13.55922956982729 usec\nrounds: 9411"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 66391.82081018313,
            "unit": "iter/sec",
            "range": "stddev: 0.00026813746982853187",
            "extra": "mean: 15.06209632145863 usec\nrounds: 8929"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 66246.92750315575,
            "unit": "iter/sec",
            "range": "stddev: 0.0002459478246629954",
            "extra": "mean: 15.095039689989605 usec\nrounds: 9165"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 67111.83766105112,
            "unit": "iter/sec",
            "range": "stddev: 0.00024069300626081855",
            "extra": "mean: 14.90050093771099 usec\nrounds: 8452"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 40829.936533433014,
            "unit": "iter/sec",
            "range": "stddev: 0.00028268572333783773",
            "extra": "mean: 24.491833318946362 usec\nrounds: 7196"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 40702.853196505304,
            "unit": "iter/sec",
            "range": "stddev: 0.0002702302639460505",
            "extra": "mean: 24.568302255672307 usec\nrounds: 7458"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 43566.329917007,
            "unit": "iter/sec",
            "range": "stddev: 0.00025779453725466317",
            "extra": "mean: 22.953505652300304 usec\nrounds: 7682"
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
        "date": 1738868541260,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 25908.590190324543,
            "unit": "iter/sec",
            "range": "stddev: 0.00025986150732209363",
            "extra": "mean: 38.59723715779201 usec\nrounds: 3217"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2572.237939911964,
            "unit": "iter/sec",
            "range": "stddev: 0.00013988184731321846",
            "extra": "mean: 388.76652291126123 usec\nrounds: 1188"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 305.2154033693973,
            "unit": "iter/sec",
            "range": "stddev: 0.0008612387211168051",
            "extra": "mean: 3.2763746159616858 msec\nrounds: 320"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 33.24750442372537,
            "unit": "iter/sec",
            "range": "stddev: 0.000509308214931883",
            "extra": "mean: 30.07744543035241 msec\nrounds: 34"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 15649.723523057126,
            "unit": "iter/sec",
            "range": "stddev: 0.0003332449944575736",
            "extra": "mean: 63.898892432615526 usec\nrounds: 5987"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 23729.7234307839,
            "unit": "iter/sec",
            "range": "stddev: 0.00043714817167027435",
            "extra": "mean: 42.14124125453263 usec\nrounds: 6581"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 36523.41868160026,
            "unit": "iter/sec",
            "range": "stddev: 0.00040215432224088784",
            "extra": "mean: 27.379693251546005 usec\nrounds: 4694"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 43408.267664969215,
            "unit": "iter/sec",
            "range": "stddev: 0.00017950185526107026",
            "extra": "mean: 23.03708610806893 usec\nrounds: 15861"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 21774.125315298505,
            "unit": "iter/sec",
            "range": "stddev: 0.00033511004039555144",
            "extra": "mean: 45.926069842970904 usec\nrounds: 11097"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 43601.05513901753,
            "unit": "iter/sec",
            "range": "stddev: 0.00023074712619391253",
            "extra": "mean: 22.9352247740703 usec\nrounds: 17158"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 24457.54659680107,
            "unit": "iter/sec",
            "range": "stddev: 0.0003315054768941675",
            "extra": "mean: 40.887175499884165 usec\nrounds: 11716"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 19139.33724066345,
            "unit": "iter/sec",
            "range": "stddev: 0.00027840864395922097",
            "extra": "mean: 52.248413172604494 usec\nrounds: 10246"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 22061.95243498652,
            "unit": "iter/sec",
            "range": "stddev: 0.00029124417029380496",
            "extra": "mean: 45.32690399668206 usec\nrounds: 10961"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 36475.19380587847,
            "unit": "iter/sec",
            "range": "stddev: 0.0002511330091064535",
            "extra": "mean: 27.415892711139932 usec\nrounds: 15737"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 21852.476283294374,
            "unit": "iter/sec",
            "range": "stddev: 0.00032024277522177836",
            "extra": "mean: 45.76140420133863 usec\nrounds: 11087"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 22415.350611859667,
            "unit": "iter/sec",
            "range": "stddev: 0.0003825132300918655",
            "extra": "mean: 44.612284559622864 usec\nrounds: 5937"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 72278.36155051114,
            "unit": "iter/sec",
            "range": "stddev: 0.0002665313979737241",
            "extra": "mean: 13.835399399599813 usec\nrounds: 9841"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 68706.87375707892,
            "unit": "iter/sec",
            "range": "stddev: 0.0002610371633894993",
            "extra": "mean: 14.554584502499928 usec\nrounds: 10083"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 64609.596631315966,
            "unit": "iter/sec",
            "range": "stddev: 0.0002938965130476068",
            "extra": "mean: 15.477576894750413 usec\nrounds: 7849"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 71939.17012596932,
            "unit": "iter/sec",
            "range": "stddev: 0.00023047490178493702",
            "extra": "mean: 13.900632968783858 usec\nrounds: 8932"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 65689.16750598195,
            "unit": "iter/sec",
            "range": "stddev: 0.00024717181930364383",
            "extra": "mean: 15.22321012682853 usec\nrounds: 8490"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 59271.922176070686,
            "unit": "iter/sec",
            "range": "stddev: 0.0002703870650471432",
            "extra": "mean: 16.87139480696175 usec\nrounds: 7916"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 40976.04232166876,
            "unit": "iter/sec",
            "range": "stddev: 0.0003256451187960891",
            "extra": "mean: 24.40450427471334 usec\nrounds: 6777"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 47038.177050459126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000072213245780873255",
            "extra": "mean: 21.2593272678759 usec\nrounds: 4508"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38884.74517817205,
            "unit": "iter/sec",
            "range": "stddev: 0.00033469473136253164",
            "extra": "mean: 25.71702592926724 usec\nrounds: 7723"
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
        "date": 1739470494232,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 21963.796167935576,
            "unit": "iter/sec",
            "range": "stddev: 0.0003674145188797652",
            "extra": "mean: 45.52947005854463 usec\nrounds: 2332"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 1914.7204199507812,
            "unit": "iter/sec",
            "range": "stddev: 0.00018689660228936325",
            "extra": "mean: 522.2694601155952 usec\nrounds: 1116"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 298.1405140766099,
            "unit": "iter/sec",
            "range": "stddev: 0.0005296111812709734",
            "extra": "mean: 3.354123149271289 msec\nrounds: 292"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 29.784799925037433,
            "unit": "iter/sec",
            "range": "stddev: 0.0009731990387038498",
            "extra": "mean: 33.574172145416654 msec\nrounds: 31"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 14164.284254971819,
            "unit": "iter/sec",
            "range": "stddev: 0.00040828518219174616",
            "extra": "mean: 70.60010813105427 usec\nrounds: 4604"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 20241.471036054085,
            "unit": "iter/sec",
            "range": "stddev: 0.0006445617818300935",
            "extra": "mean: 49.40352399382442 usec\nrounds: 5740"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 33277.74655857695,
            "unit": "iter/sec",
            "range": "stddev: 0.0004987554295406496",
            "extra": "mean: 30.050111663653546 usec\nrounds: 5769"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 39511.461371048994,
            "unit": "iter/sec",
            "range": "stddev: 0.00025353524839888397",
            "extra": "mean: 25.309111971563887 usec\nrounds: 10428"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 19415.480336951434,
            "unit": "iter/sec",
            "range": "stddev: 0.00039665001261453644",
            "extra": "mean: 51.50529282022478 usec\nrounds: 9257"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 38699.50168587716,
            "unit": "iter/sec",
            "range": "stddev: 0.0003144733578053469",
            "extra": "mean: 25.840126007744846 usec\nrounds: 16528"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 21140.414523408053,
            "unit": "iter/sec",
            "range": "stddev: 0.0005042506656932873",
            "extra": "mean: 47.30276215221487 usec\nrounds: 8630"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 16530.317356352964,
            "unit": "iter/sec",
            "range": "stddev: 0.0004597239369523802",
            "extra": "mean: 60.494906325296775 usec\nrounds: 5262"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 19965.438150615537,
            "unit": "iter/sec",
            "range": "stddev: 0.0003351884020341267",
            "extra": "mean: 50.08655419711738 usec\nrounds: 9693"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 31469.685570800455,
            "unit": "iter/sec",
            "range": "stddev: 0.0003541778543668939",
            "extra": "mean: 31.776612376701426 usec\nrounds: 13168"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 19062.942984464007,
            "unit": "iter/sec",
            "range": "stddev: 0.0004737885770342732",
            "extra": "mean: 52.45779735138398 usec\nrounds: 6488"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 19405.11932251415,
            "unit": "iter/sec",
            "range": "stddev: 0.0005033189544305093",
            "extra": "mean: 51.53279314494 usec\nrounds: 4475"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 61133.05691459353,
            "unit": "iter/sec",
            "range": "stddev: 0.0003405779203363839",
            "extra": "mean: 16.357762076204676 usec\nrounds: 8579"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 64115.35456904825,
            "unit": "iter/sec",
            "range": "stddev: 0.00030866637462937177",
            "extra": "mean: 15.596887933031116 usec\nrounds: 8965"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 57962.243064564704,
            "unit": "iter/sec",
            "range": "stddev: 0.00033622880716316285",
            "extra": "mean: 17.25261044307913 usec\nrounds: 7238"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 55483.279893423605,
            "unit": "iter/sec",
            "range": "stddev: 0.00033483004683105465",
            "extra": "mean: 18.023447819250666 usec\nrounds: 8340"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 54308.47554066193,
            "unit": "iter/sec",
            "range": "stddev: 0.0003761950558144452",
            "extra": "mean: 18.413332174114856 usec\nrounds: 7254"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 56133.03589214775,
            "unit": "iter/sec",
            "range": "stddev: 0.0003305490312337868",
            "extra": "mean: 17.814821238626187 usec\nrounds: 7828"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36732.873991031505,
            "unit": "iter/sec",
            "range": "stddev: 0.0003925960440679351",
            "extra": "mean: 27.22357091482018 usec\nrounds: 6033"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 42255.52641550911,
            "unit": "iter/sec",
            "range": "stddev: 0.000008304057173541984",
            "extra": "mean: 23.66554353545974 usec\nrounds: 2401"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 35658.68086193157,
            "unit": "iter/sec",
            "range": "stddev: 0.0004189320723605436",
            "extra": "mean: 28.04366218346507 usec\nrounds: 6651"
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
        "date": 1740359239461,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 21749.041045671787,
            "unit": "iter/sec",
            "range": "stddev: 0.000040580620718611996",
            "extra": "mean: 45.97903870336421 usec\nrounds: 616"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 1436.4842677854494,
            "unit": "iter/sec",
            "range": "stddev: 0.0007859594521359893",
            "extra": "mean: 696.1440667510033 usec\nrounds: 764"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 152.59456070028273,
            "unit": "iter/sec",
            "range": "stddev: 0.0021850702693115513",
            "extra": "mean: 6.553313534970235 msec\nrounds: 99"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 19.140433651143432,
            "unit": "iter/sec",
            "range": "stddev: 0.0044435072885481595",
            "extra": "mean: 52.24542025672762 msec\nrounds: 19"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 12332.745820492146,
            "unit": "iter/sec",
            "range": "stddev: 0.0003687705622009495",
            "extra": "mean: 81.08494365775346 usec\nrounds: 4917"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 16830.62644983962,
            "unit": "iter/sec",
            "range": "stddev: 0.0007110567122790738",
            "extra": "mean: 59.41549490034158 usec\nrounds: 4657"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 29918.579244064244,
            "unit": "iter/sec",
            "range": "stddev: 0.0004603594578873208",
            "extra": "mean: 33.42404703921216 usec\nrounds: 5494"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 32597.365650517582,
            "unit": "iter/sec",
            "range": "stddev: 0.000319910148624297",
            "extra": "mean: 30.67732560726489 usec\nrounds: 10380"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 13645.135845505823,
            "unit": "iter/sec",
            "range": "stddev: 0.000507741545040925",
            "extra": "mean: 73.28618866988862 usec\nrounds: 6275"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 30000.500103810085,
            "unit": "iter/sec",
            "range": "stddev: 0.00032415118888809414",
            "extra": "mean: 33.33277767169619 usec\nrounds: 11822"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 16346.463250788958,
            "unit": "iter/sec",
            "range": "stddev: 0.0004956816756577379",
            "extra": "mean: 61.175312644570695 usec\nrounds: 6389"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 12353.303904579172,
            "unit": "iter/sec",
            "range": "stddev: 0.00034154949965308737",
            "extra": "mean: 80.95000396042357 usec\nrounds: 6809"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 14257.08976082045,
            "unit": "iter/sec",
            "range": "stddev: 0.0004236818841946133",
            "extra": "mean: 70.14054177789319 usec\nrounds: 7311"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 23776.177697880517,
            "unit": "iter/sec",
            "range": "stddev: 0.0003433739121365318",
            "extra": "mean: 42.05890503960791 usec\nrounds: 11159"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 13017.569614885788,
            "unit": "iter/sec",
            "range": "stddev: 0.000577064503517306",
            "extra": "mean: 76.81925502103594 usec\nrounds: 4340"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 17045.911193641947,
            "unit": "iter/sec",
            "range": "stddev: 0.0004181971418129748",
            "extra": "mean: 58.66509502718728 usec\nrounds: 4111"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 63592.233446149716,
            "unit": "iter/sec",
            "range": "stddev: 0.00038797285899477553",
            "extra": "mean: 15.725190731770823 usec\nrounds: 8604"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 57012.76846646459,
            "unit": "iter/sec",
            "range": "stddev: 0.00040462443638427796",
            "extra": "mean: 17.53993056113752 usec\nrounds: 8495"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 53707.221640433556,
            "unit": "iter/sec",
            "range": "stddev: 0.00045096170289106197",
            "extra": "mean: 18.619469960575074 usec\nrounds: 7148"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 62427.103474260744,
            "unit": "iter/sec",
            "range": "stddev: 0.00037263009184265066",
            "extra": "mean: 16.018683301753843 usec\nrounds: 7682"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 53579.83935413687,
            "unit": "iter/sec",
            "range": "stddev: 0.0004251278826747596",
            "extra": "mean: 18.663736436208453 usec\nrounds: 6976"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 53795.69438144269,
            "unit": "iter/sec",
            "range": "stddev: 0.0004110711499040469",
            "extra": "mean: 18.58884826189657 usec\nrounds: 6997"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 35896.97341919974,
            "unit": "iter/sec",
            "range": "stddev: 0.00043189203067652514",
            "extra": "mean: 27.857501754316235 usec\nrounds: 5900"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 34029.98527646279,
            "unit": "iter/sec",
            "range": "stddev: 0.00040552132191965434",
            "extra": "mean: 29.385848741217675 usec\nrounds: 5989"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 35857.125727681494,
            "unit": "iter/sec",
            "range": "stddev: 0.00042018915992287075",
            "extra": "mean: 27.888459537848732 usec\nrounds: 5912"
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
        "date": 1740520224023,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 23603.832790903263,
            "unit": "iter/sec",
            "range": "stddev: 0.00047162321500435585",
            "extra": "mean: 42.36600084649779 usec\nrounds: 857"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 1945.0913761259878,
            "unit": "iter/sec",
            "range": "stddev: 0.0000273809219068959",
            "extra": "mean: 514.1146643669185 usec\nrounds: 1466"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 163.54777215394247,
            "unit": "iter/sec",
            "range": "stddev: 0.0027977242052098597",
            "extra": "mean: 6.114421412348747 msec\nrounds: 192"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 18.98913937459572,
            "unit": "iter/sec",
            "range": "stddev: 0.004711289311726604",
            "extra": "mean: 52.66168098896742 msec\nrounds: 20"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 12055.751701373847,
            "unit": "iter/sec",
            "range": "stddev: 0.0003905619969665665",
            "extra": "mean: 82.94795917918931 usec\nrounds: 4762"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 17640.908225114184,
            "unit": "iter/sec",
            "range": "stddev: 0.0006178064676496536",
            "extra": "mean: 56.686423807611376 usec\nrounds: 5797"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 28934.631692033898,
            "unit": "iter/sec",
            "range": "stddev: 0.0005564218196773235",
            "extra": "mean: 34.56066110132357 usec\nrounds: 5394"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 30241.21224845672,
            "unit": "iter/sec",
            "range": "stddev: 0.0003688089671529852",
            "extra": "mean: 33.06745747439514 usec\nrounds: 9807"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 13745.730650623158,
            "unit": "iter/sec",
            "range": "stddev: 0.0004873685026081626",
            "extra": "mean: 72.74986142367523 usec\nrounds: 7460"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 31284.202346066286,
            "unit": "iter/sec",
            "range": "stddev: 0.0003169939689649186",
            "extra": "mean: 31.96501508774256 usec\nrounds: 11555"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 15671.91023791262,
            "unit": "iter/sec",
            "range": "stddev: 0.0005476246274145088",
            "extra": "mean: 63.808430805126434 usec\nrounds: 7165"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 12175.885415383644,
            "unit": "iter/sec",
            "range": "stddev: 0.0004338645432692989",
            "extra": "mean: 82.12955081989752 usec\nrounds: 6516"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 14678.16934558782,
            "unit": "iter/sec",
            "range": "stddev: 0.0003819494715263857",
            "extra": "mean: 68.12838688910445 usec\nrounds: 6957"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 23465.127221680123,
            "unit": "iter/sec",
            "range": "stddev: 0.0003300290101798601",
            "extra": "mean: 42.61643205906297 usec\nrounds: 9848"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 13728.648054533054,
            "unit": "iter/sec",
            "range": "stddev: 0.00043645755993268134",
            "extra": "mean: 72.84038428458442 usec\nrounds: 6732"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 15207.31457323192,
            "unit": "iter/sec",
            "range": "stddev: 0.0005768537787532097",
            "extra": "mean: 65.7578295750001 usec\nrounds: 4374"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 60700.26470312495,
            "unit": "iter/sec",
            "range": "stddev: 0.0004468433079705268",
            "extra": "mean: 16.474392737673156 usec\nrounds: 8466"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 59744.6047088178,
            "unit": "iter/sec",
            "range": "stddev: 0.0004323764527770024",
            "extra": "mean: 16.73791306970365 usec\nrounds: 6913"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 55718.145386283875,
            "unit": "iter/sec",
            "range": "stddev: 0.00040675947701884833",
            "extra": "mean: 17.94747461652178 usec\nrounds: 7347"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 50468.89419907531,
            "unit": "iter/sec",
            "range": "stddev: 0.0005128732201413622",
            "extra": "mean: 19.814184873072215 usec\nrounds: 4188"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 55891.434703135536,
            "unit": "iter/sec",
            "range": "stddev: 0.0003505853792108819",
            "extra": "mean: 17.891829138247182 usec\nrounds: 7157"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 53473.904429126764,
            "unit": "iter/sec",
            "range": "stddev: 0.00041213348152289997",
            "extra": "mean: 18.700710387164264 usec\nrounds: 7408"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 33499.397160587716,
            "unit": "iter/sec",
            "range": "stddev: 0.0005505119152943769",
            "extra": "mean: 29.851283448661796 usec\nrounds: 5179"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 32772.5472842953,
            "unit": "iter/sec",
            "range": "stddev: 0.0004718239157501535",
            "extra": "mean: 30.51334372409931 usec\nrounds: 5005"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 36384.40299651801,
            "unit": "iter/sec",
            "range": "stddev: 0.0003956718691582461",
            "extra": "mean: 27.484304197479894 usec\nrounds: 6543"
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
        "date": 1750089703809,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47534.199258252775,
            "unit": "iter/sec",
            "range": "stddev: 0.000013081080240377823",
            "extra": "mean: 21.037484918321883 usec\nrounds: 875"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2082.5588368108774,
            "unit": "iter/sec",
            "range": "stddev: 0.001081477351453081",
            "extra": "mean: 480.1785103614879 usec\nrounds: 1709"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 229.74778209737264,
            "unit": "iter/sec",
            "range": "stddev: 0.0001624268717321115",
            "extra": "mean: 4.352599145336584 msec\nrounds: 220"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 20.715078654812064,
            "unit": "iter/sec",
            "range": "stddev: 0.01209575874305131",
            "extra": "mean: 48.27401414513588 msec\nrounds: 23"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 10447.882691525772,
            "unit": "iter/sec",
            "range": "stddev: 0.0012604639799531443",
            "extra": "mean: 95.71317266139438 usec\nrounds: 5203"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 18105.782141283067,
            "unit": "iter/sec",
            "range": "stddev: 0.0011477691860438198",
            "extra": "mean: 55.230974955779224 usec\nrounds: 5494"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 25674.280694520807,
            "unit": "iter/sec",
            "range": "stddev: 0.0010918256868084305",
            "extra": "mean: 38.94948457946134 usec\nrounds: 3911"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 34953.61722681965,
            "unit": "iter/sec",
            "range": "stddev: 0.0006362715801936179",
            "extra": "mean: 28.609342303854813 usec\nrounds: 8272"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 15949.819548829657,
            "unit": "iter/sec",
            "range": "stddev: 0.0007841319877191853",
            "extra": "mean: 62.696634086582904 usec\nrounds: 6829"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 32093.031296081324,
            "unit": "iter/sec",
            "range": "stddev: 0.0006693854827709044",
            "extra": "mean: 31.159412483485273 usec\nrounds: 13425"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 16564.115326982654,
            "unit": "iter/sec",
            "range": "stddev: 0.0010454300750903534",
            "extra": "mean: 60.37147051077442 usec\nrounds: 7724"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 16210.627791582534,
            "unit": "iter/sec",
            "range": "stddev: 0.00001117084762564144",
            "extra": "mean: 61.68792552989564 usec\nrounds: 4474"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 16812.418391115494,
            "unit": "iter/sec",
            "range": "stddev: 0.0008343763299384015",
            "extra": "mean: 59.47984262207328 usec\nrounds: 7181"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 25138.135263104607,
            "unit": "iter/sec",
            "range": "stddev: 0.0007267893450034235",
            "extra": "mean: 39.78019807490279 usec\nrounds: 11672"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 15785.764111590237,
            "unit": "iter/sec",
            "range": "stddev: 0.0008394369146921975",
            "extra": "mean: 63.34821633789518 usec\nrounds: 7630"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 15675.814919050186,
            "unit": "iter/sec",
            "range": "stddev: 0.0011132723951393457",
            "extra": "mean: 63.79253679403552 usec\nrounds: 3240"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 44642.75642595974,
            "unit": "iter/sec",
            "range": "stddev: 0.0008139850490820042",
            "extra": "mean: 22.40005053582445 usec\nrounds: 8473"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 57168.603478277364,
            "unit": "iter/sec",
            "range": "stddev: 0.000738401223456071",
            "extra": "mean: 17.492118735766827 usec\nrounds: 9139"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 50220.778330145906,
            "unit": "iter/sec",
            "range": "stddev: 0.0007862151643865434",
            "extra": "mean: 19.912076898253336 usec\nrounds: 8116"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 41278.57784604728,
            "unit": "iter/sec",
            "range": "stddev: 0.0009054842334063783",
            "extra": "mean: 24.22564080888647 usec\nrounds: 8406"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 48698.00296937938,
            "unit": "iter/sec",
            "range": "stddev: 0.0007863852413605206",
            "extra": "mean: 20.53472296654107 usec\nrounds: 8126"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 47154.38179051619,
            "unit": "iter/sec",
            "range": "stddev: 0.0007501429703013841",
            "extra": "mean: 21.206936917177917 usec\nrounds: 7880"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 36532.58896476427,
            "unit": "iter/sec",
            "range": "stddev: 0.0008377975128362728",
            "extra": "mean: 27.372820496365623 usec\nrounds: 6160"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 34676.362269648555,
            "unit": "iter/sec",
            "range": "stddev: 0.0008599395533621481",
            "extra": "mean: 28.838088384930664 usec\nrounds: 5816"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38404.48620357846,
            "unit": "iter/sec",
            "range": "stddev: 0.000771227622719278",
            "extra": "mean: 26.038624620548152 usec\nrounds: 7334"
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
        "date": 1750090616281,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 48115.39350662115,
            "unit": "iter/sec",
            "range": "stddev: 0.000014256448135783263",
            "extra": "mean: 20.7833694608024 usec\nrounds: 890"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2091.1631550388597,
            "unit": "iter/sec",
            "range": "stddev: 0.0010351185188109966",
            "extra": "mean: 478.20276365830347 usec\nrounds: 1716"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 229.9872178805891,
            "unit": "iter/sec",
            "range": "stddev: 0.00012518337925777588",
            "extra": "mean: 4.348067728351785 msec\nrounds: 219"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 20.576423591658987,
            "unit": "iter/sec",
            "range": "stddev: 0.011531061067993918",
            "extra": "mean: 48.59931054322616 msec\nrounds: 23"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 10256.110099953117,
            "unit": "iter/sec",
            "range": "stddev: 0.0013347394473935687",
            "extra": "mean: 97.5028534458275 usec\nrounds: 4894"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 18443.840378287157,
            "unit": "iter/sec",
            "range": "stddev: 0.0011132788101221103",
            "extra": "mean: 54.21864316160754 usec\nrounds: 6096"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 30063.16685024552,
            "unit": "iter/sec",
            "range": "stddev: 0.0009082827808562364",
            "extra": "mean: 33.26329541333178 usec\nrounds: 5828"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 28121.91008279733,
            "unit": "iter/sec",
            "range": "stddev: 0.0009049667736377425",
            "extra": "mean: 35.55946225045779 usec\nrounds: 8141"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 18858.266128064046,
            "unit": "iter/sec",
            "range": "stddev: 0.000010626774980056104",
            "extra": "mean: 53.027144341326476 usec\nrounds: 4288"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 30750.98476241176,
            "unit": "iter/sec",
            "range": "stddev: 0.0007751339272808974",
            "extra": "mean: 32.51928377989191 usec\nrounds: 13149"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 16747.899441090147,
            "unit": "iter/sec",
            "range": "stddev: 0.0010624068487433418",
            "extra": "mean: 59.708980431692176 usec\nrounds: 7849"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 14289.493184229006,
            "unit": "iter/sec",
            "range": "stddev: 0.0008102813811019836",
            "extra": "mean: 69.98148829404795 usec\nrounds: 7271"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 17148.158767866742,
            "unit": "iter/sec",
            "range": "stddev: 0.0007699329159764242",
            "extra": "mean: 58.31529865899425 usec\nrounds: 7372"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 23955.881326974522,
            "unit": "iter/sec",
            "range": "stddev: 0.0008299813632751385",
            "extra": "mean: 41.743402647181746 usec\nrounds: 11282"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 15548.009478644964,
            "unit": "iter/sec",
            "range": "stddev: 0.000949120373412994",
            "extra": "mean: 64.31691473905325 usec\nrounds: 7073"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 16923.69878856886,
            "unit": "iter/sec",
            "range": "stddev: 0.0010141230599230197",
            "extra": "mean: 59.08873778085979 usec\nrounds: 4197"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 59662.716681925456,
            "unit": "iter/sec",
            "range": "stddev: 0.0006765019077972321",
            "extra": "mean: 16.760886121415005 usec\nrounds: 9324"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 40765.036720091004,
            "unit": "iter/sec",
            "range": "stddev: 0.000963822072116689",
            "extra": "mean: 24.530825444029368 usec\nrounds: 8503"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 49603.13448306697,
            "unit": "iter/sec",
            "range": "stddev: 0.0008243945628387164",
            "extra": "mean: 20.160016305852004 usec\nrounds: 8675"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 53274.45138875423,
            "unit": "iter/sec",
            "range": "stddev: 0.0007686957140947589",
            "extra": "mean: 18.770723563210474 usec\nrounds: 8771"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 37477.73485911374,
            "unit": "iter/sec",
            "range": "stddev: 0.0010085826551413618",
            "extra": "mean: 26.682509061959024 usec\nrounds: 4478"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 84055.17154137653,
            "unit": "iter/sec",
            "range": "stddev: 0.000007611248431873121",
            "extra": "mean: 11.89694794100498 usec\nrounds: 2147"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 37635.518133140125,
            "unit": "iter/sec",
            "range": "stddev: 0.0007750482422304348",
            "extra": "mean: 26.57064522035756 usec\nrounds: 6430"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 37307.88791556202,
            "unit": "iter/sec",
            "range": "stddev: 0.0007690766587604287",
            "extra": "mean: 26.80398317544199 usec\nrounds: 6827"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 38765.59495353937,
            "unit": "iter/sec",
            "range": "stddev: 0.0007471163215066013",
            "extra": "mean: 25.796069973864753 usec\nrounds: 6923"
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
        "date": 1750165847250,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 48900.587931014765,
            "unit": "iter/sec",
            "range": "stddev: 0.000012200873761297189",
            "extra": "mean: 20.449651881705883 usec\nrounds: 860"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2095.5624014105874,
            "unit": "iter/sec",
            "range": "stddev: 0.0010129236380334165",
            "extra": "mean: 477.1988652434637 usec\nrounds: 1758"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 230.14662960384263,
            "unit": "iter/sec",
            "range": "stddev: 0.00016885478676874848",
            "extra": "mean: 4.345056026765745 msec\nrounds: 219"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 20.725449374418044,
            "unit": "iter/sec",
            "range": "stddev: 0.011743943908535885",
            "extra": "mean: 48.24985851618377 msec\nrounds: 22"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 10852.160657458324,
            "unit": "iter/sec",
            "range": "stddev: 0.0012004615013663444",
            "extra": "mean: 92.14754845273451 usec\nrounds: 5420"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 15266.848433820689,
            "unit": "iter/sec",
            "range": "stddev: 0.0014818374804366",
            "extra": "mean: 65.50140353687519 usec\nrounds: 6186"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 45614.7211333409,
            "unit": "iter/sec",
            "range": "stddev: 0.000009605787161776425",
            "extra": "mean: 21.922747199896303 usec\nrounds: 5694"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 27861.023516889098,
            "unit": "iter/sec",
            "range": "stddev: 0.0010577714171305828",
            "extra": "mean: 35.892435875294 usec\nrounds: 10288"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 16076.646587361625,
            "unit": "iter/sec",
            "range": "stddev: 0.0008338083791491417",
            "extra": "mean: 62.202026682985775 usec\nrounds: 7062"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 31280.199182111905,
            "unit": "iter/sec",
            "range": "stddev: 0.0007398158223603945",
            "extra": "mean: 31.96910589277406 usec\nrounds: 12857"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 15915.490164373197,
            "unit": "iter/sec",
            "range": "stddev: 0.0012524485036258216",
            "extra": "mean: 62.831869434879145 usec\nrounds: 4202"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 14309.687703462732,
            "unit": "iter/sec",
            "range": "stddev: 0.0007129011597286128",
            "extra": "mean: 69.88272705336642 usec\nrounds: 7046"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 17190.885136548874,
            "unit": "iter/sec",
            "range": "stddev: 0.0007594824025823944",
            "extra": "mean: 58.17036133142084 usec\nrounds: 7422"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 24545.5661920283,
            "unit": "iter/sec",
            "range": "stddev: 0.0008246134608924866",
            "extra": "mean: 40.74055542971225 usec\nrounds: 11280"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 15773.305686623806,
            "unit": "iter/sec",
            "range": "stddev: 0.0008918272898886488",
            "extra": "mean: 63.39825144250056 usec\nrounds: 7689"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 17239.225562758642,
            "unit": "iter/sec",
            "range": "stddev: 0.0009767372687814245",
            "extra": "mean: 58.00724611204512 usec\nrounds: 4227"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 60028.699003797614,
            "unit": "iter/sec",
            "range": "stddev: 0.0006610864865920941",
            "extra": "mean: 16.658698532459226 usec\nrounds: 9275"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 46228.131182749974,
            "unit": "iter/sec",
            "range": "stddev: 0.0008382709506050376",
            "extra": "mean: 21.6318500102628 usec\nrounds: 9825"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 51800.81383578685,
            "unit": "iter/sec",
            "range": "stddev: 0.0007746619642033501",
            "extra": "mean: 19.304716006394962 usec\nrounds: 8684"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 43105.726672326484,
            "unit": "iter/sec",
            "range": "stddev: 0.0009053220493353587",
            "extra": "mean: 23.198773740705583 usec\nrounds: 9499"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 45454.72485529232,
            "unit": "iter/sec",
            "range": "stddev: 0.0008859360892917511",
            "extra": "mean: 21.999913170381216 usec\nrounds: 7228"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 48185.27286948772,
            "unit": "iter/sec",
            "range": "stddev: 0.0007506493603573513",
            "extra": "mean: 20.753228952517322 usec\nrounds: 8275"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 35155.299215351966,
            "unit": "iter/sec",
            "range": "stddev: 0.0008936816160880394",
            "extra": "mean: 28.44521373219631 usec\nrounds: 5843"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 31089.696588034592,
            "unit": "iter/sec",
            "range": "stddev: 0.0010029028578564835",
            "extra": "mean: 32.16499708089359 usec\nrounds: 4365"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37517.39020841485,
            "unit": "iter/sec",
            "range": "stddev: 0.0007849157611410761",
            "extra": "mean: 26.654306028347037 usec\nrounds: 6708"
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
        "date": 1750968943476,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 48458.38214993146,
            "unit": "iter/sec",
            "range": "stddev: 0.000012886948497119722",
            "extra": "mean: 20.63626467978181 usec\nrounds: 879"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2018.1670328621099,
            "unit": "iter/sec",
            "range": "stddev: 0.0010673507202414681",
            "extra": "mean: 495.4991255514797 usec\nrounds: 1572"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 224.56789980134502,
            "unit": "iter/sec",
            "range": "stddev: 0.00005563337838894613",
            "extra": "mean: 4.452996180151348 msec\nrounds: 216"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 19.955146763359437,
            "unit": "iter/sec",
            "range": "stddev: 0.012297494738333229",
            "extra": "mean: 50.11238513345069 msec\nrounds: 22"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 11621.685342068968,
            "unit": "iter/sec",
            "range": "stddev: 0.0009981557129308731",
            "extra": "mean: 86.04603984416373 usec\nrounds: 4457"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 16453.245614752148,
            "unit": "iter/sec",
            "range": "stddev: 0.0011795350455350451",
            "extra": "mean: 60.77828189128775 usec\nrounds: 5937"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 28289.832105276895,
            "unit": "iter/sec",
            "range": "stddev: 0.0009679513553531825",
            "extra": "mean: 35.34838935341261 usec\nrounds: 5084"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 29480.35588644195,
            "unit": "iter/sec",
            "range": "stddev: 0.0008021069545832788",
            "extra": "mean: 33.920893080530995 usec\nrounds: 9602"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 16013.610680011821,
            "unit": "iter/sec",
            "range": "stddev: 0.0008216898071911789",
            "extra": "mean: 62.44687846996301 usec\nrounds: 7574"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 30333.337893808122,
            "unit": "iter/sec",
            "range": "stddev: 0.0008019045707322261",
            "extra": "mean: 32.9670280105945 usec\nrounds: 11955"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 18479.934947008514,
            "unit": "iter/sec",
            "range": "stddev: 0.0009450125014542029",
            "extra": "mean: 54.11274459934597 usec\nrounds: 7362"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 14188.86186417765,
            "unit": "iter/sec",
            "range": "stddev: 0.0008127253106862305",
            "extra": "mean: 70.47781630214338 usec\nrounds: 6151"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 16953.97571093138,
            "unit": "iter/sec",
            "range": "stddev: 0.0007500902783585514",
            "extra": "mean: 58.983215326611095 usec\nrounds: 6994"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 27568.87310942953,
            "unit": "iter/sec",
            "range": "stddev: 0.0006522210211953768",
            "extra": "mean: 36.27279200098914 usec\nrounds: 10690"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 16065.909235460354,
            "unit": "iter/sec",
            "range": "stddev: 0.0008340650984098552",
            "extra": "mean: 62.24359825168313 usec\nrounds: 7173"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 15137.820079158944,
            "unit": "iter/sec",
            "range": "stddev: 0.0011302614537808315",
            "extra": "mean: 66.05970970528008 usec\nrounds: 4618"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 57383.75159873879,
            "unit": "iter/sec",
            "range": "stddev: 0.0007226808588969802",
            "extra": "mean: 17.426535772575363 usec\nrounds: 9137"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 42638.70605579306,
            "unit": "iter/sec",
            "range": "stddev: 0.0009289190472722174",
            "extra": "mean: 23.452869294192297 usec\nrounds: 8933"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 50166.93382987362,
            "unit": "iter/sec",
            "range": "stddev: 0.0008108383195370492",
            "extra": "mean: 19.93344866144711 usec\nrounds: 8418"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 57635.24969127524,
            "unit": "iter/sec",
            "range": "stddev: 0.000704545220967972",
            "extra": "mean: 17.350493063819915 usec\nrounds: 9333"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 47129.080349447664,
            "unit": "iter/sec",
            "range": "stddev: 0.0007970284167299047",
            "extra": "mean: 21.218321948684483 usec\nrounds: 6930"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 49632.92079392423,
            "unit": "iter/sec",
            "range": "stddev: 0.0006714431984491563",
            "extra": "mean: 20.147917632169936 usec\nrounds: 7647"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 38512.55053920679,
            "unit": "iter/sec",
            "range": "stddev: 0.0007678838227438957",
            "extra": "mean: 25.96556151174599 usec\nrounds: 6568"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 29319.211444687997,
            "unit": "iter/sec",
            "range": "stddev: 0.0009570918264912802",
            "extra": "mean: 34.10732931499692 usec\nrounds: 6704"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 37186.693567594935,
            "unit": "iter/sec",
            "range": "stddev: 0.0008543712688099027",
            "extra": "mean: 26.891339456740937 usec\nrounds: 6890"
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
          "id": "2165259e9966447c52305e486b08e12025b22c81",
          "message": "Merge pull request #104 from amsdal/feature/elasticsearch-connection\n\nElasticsearch connection",
          "timestamp": "2025-08-06T22:29:16+03:00",
          "tree_id": "ba148c4870f3f5782d98573cbff129b643a3f091",
          "url": "https://github.com/amsdal/amsdal-glue/commit/2165259e9966447c52305e486b08e12025b22c81"
        },
        "date": 1754508617258,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 46296.10562403716,
            "unit": "iter/sec",
            "range": "stddev: 0.000019904760591932773",
            "extra": "mean: 21.600088960415608 usec\nrounds: 518"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2084.3806408143655,
            "unit": "iter/sec",
            "range": "stddev: 0.00003590749805234713",
            "extra": "mean: 479.7588215985833 usec\nrounds: 1658"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 203.79464034643814,
            "unit": "iter/sec",
            "range": "stddev: 0.0038004282786588497",
            "extra": "mean: 4.906900389038999 msec\nrounds: 207"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 18.24305077923832,
            "unit": "iter/sec",
            "range": "stddev: 0.018266571674287687",
            "extra": "mean: 54.81539311056787 msec\nrounds: 22"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 11249.258704025751,
            "unit": "iter/sec",
            "range": "stddev: 0.001160028060449493",
            "extra": "mean: 88.89474642823636 usec\nrounds: 5297"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 15454.071115740771,
            "unit": "iter/sec",
            "range": "stddev: 0.0014005548196213014",
            "extra": "mean: 64.7078683998968 usec\nrounds: 6272"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 28403.611981865804,
            "unit": "iter/sec",
            "range": "stddev: 0.0010064227124942887",
            "extra": "mean: 35.206789919480904 usec\nrounds: 6017"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 28248.320824369,
            "unit": "iter/sec",
            "range": "stddev: 0.0009098531781145638",
            "extra": "mean: 35.40033427889028 usec\nrounds: 10216"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 15392.867423664751,
            "unit": "iter/sec",
            "range": "stddev: 0.0009521949844522948",
            "extra": "mean: 64.96515382589573 usec\nrounds: 7666"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 34657.435827282156,
            "unit": "iter/sec",
            "range": "stddev: 0.0006631929945855305",
            "extra": "mean: 28.85383687886122 usec\nrounds: 12829"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 15995.789526289125,
            "unit": "iter/sec",
            "range": "stddev: 0.0011694300486123738",
            "extra": "mean: 62.51645149221907 usec\nrounds: 8009"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 13824.784931063743,
            "unit": "iter/sec",
            "range": "stddev: 0.0008862824306851033",
            "extra": "mean: 72.33385582390072 usec\nrounds: 7950"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 14951.323933609458,
            "unit": "iter/sec",
            "range": "stddev: 0.0011171656344564473",
            "extra": "mean: 66.88370905750192 usec\nrounds: 4603"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 23670.144388259934,
            "unit": "iter/sec",
            "range": "stddev: 0.00089093357857485",
            "extra": "mean: 42.247313053822616 usec\nrounds: 12139"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 15278.871287522245,
            "unit": "iter/sec",
            "range": "stddev: 0.0010276111569006332",
            "extra": "mean: 65.4498608687585 usec\nrounds: 8111"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 16168.018668716748,
            "unit": "iter/sec",
            "range": "stddev: 0.0012390916636823082",
            "extra": "mean: 61.85049760827433 usec\nrounds: 4368"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 51370.60885135163,
            "unit": "iter/sec",
            "range": "stddev: 0.0008704374208507818",
            "extra": "mean: 19.46638403476288 usec\nrounds: 8198"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 52526.4242290063,
            "unit": "iter/sec",
            "range": "stddev: 0.000839969141571762",
            "extra": "mean: 19.038036848656777 usec\nrounds: 8209"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 49489.66477979925,
            "unit": "iter/sec",
            "range": "stddev: 0.0008264526165009836",
            "extra": "mean: 20.206239109709657 usec\nrounds: 8351"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 42379.88552022974,
            "unit": "iter/sec",
            "range": "stddev: 0.0009799326998149508",
            "extra": "mean: 23.59609960538135 usec\nrounds: 5276"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 38956.88904338463,
            "unit": "iter/sec",
            "range": "stddev: 0.0009730050452826484",
            "extra": "mean: 25.669400831425282 usec\nrounds: 4779"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 37897.64054612925,
            "unit": "iter/sec",
            "range": "stddev: 0.0010082071473039545",
            "extra": "mean: 26.386866981409923 usec\nrounds: 4787"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 35414.096553070216,
            "unit": "iter/sec",
            "range": "stddev: 0.0008924435856287865",
            "extra": "mean: 28.237343242723647 usec\nrounds: 6278"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 32754.35718113369,
            "unit": "iter/sec",
            "range": "stddev: 0.0010012870810308732",
            "extra": "mean: 30.53028928242847 usec\nrounds: 5872"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 36408.80026033649,
            "unit": "iter/sec",
            "range": "stddev: 0.0008831140652645837",
            "extra": "mean: 27.46588717149775 usec\nrounds: 7366"
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
          "id": "0a9f6e121cf0bbba9c515ebd03fea0d30fdf97ec",
          "message": "Merge pull request #105 from amsdal/fix-for-connections-conflict\n\nIgnore KeyError when popping from connections in ConnectionPool",
          "timestamp": "2025-08-26T20:44:18+03:00",
          "tree_id": "5874998bdf28c7265722bd4825508d8d3e46a07d",
          "url": "https://github.com/amsdal/amsdal-glue/commit/0a9f6e121cf0bbba9c515ebd03fea0d30fdf97ec"
        },
        "date": 1756230318091,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark",
            "value": 47013.48945086162,
            "unit": "iter/sec",
            "range": "stddev: 0.000019541700782703434",
            "extra": "mean: 21.27049090974618 usec\nrounds: 573"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_100",
            "value": 2162.76483809115,
            "unit": "iter/sec",
            "range": "stddev: 0.000033194425202192785",
            "extra": "mean: 462.3711197758315 usec\nrounds: 1766"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_1000",
            "value": 213.9755380096531,
            "unit": "iter/sec",
            "range": "stddev: 0.003548011065450357",
            "extra": "mean: 4.673431408570109 msec\nrounds: 217"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_benchmark_10000",
            "value": 18.831792547077974,
            "unit": "iter/sec",
            "range": "stddev: 0.01896959734047054",
            "extra": "mean: 53.101689470085226 msec\nrounds: 22"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_insert_multiple_benchmark",
            "value": 11370.963702141962,
            "unit": "iter/sec",
            "range": "stddev: 0.0011969880299788978",
            "extra": "mean: 87.94329365519202 usec\nrounds: 5146"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_update_benchmark",
            "value": 10782.331370533759,
            "unit": "iter/sec",
            "range": "stddev: 0.002211588227779081",
            "extra": "mean: 92.74432083703405 usec\nrounds: 1736"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_mutations.py::test_delete_benchmark",
            "value": 30215.39415795441,
            "unit": "iter/sec",
            "range": "stddev: 0.0008804646961864859",
            "extra": "mean: 33.095712562026705 usec\nrounds: 5822"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_simple_query_benchmark",
            "value": 31742.506335094964,
            "unit": "iter/sec",
            "range": "stddev: 0.0008676650639947935",
            "extra": "mean: 31.503498477509506 usec\nrounds: 8546"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_join_query_benchmark",
            "value": 15945.469660923425,
            "unit": "iter/sec",
            "range": "stddev: 0.000903616758161475",
            "extra": "mean: 62.713737585957595 usec\nrounds: 7262"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_query_distinct_benchmark",
            "value": 28699.328075777597,
            "unit": "iter/sec",
            "range": "stddev: 0.0009333798435826011",
            "extra": "mean: 34.84402134292496 usec\nrounds: 11846"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_benchmark",
            "value": 17627.75105946647,
            "unit": "iter/sec",
            "range": "stddev: 0.0010794727490689208",
            "extra": "mean: 56.72873395060677 usec\nrounds: 7010"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_filter_conditions_join_benchmark",
            "value": 14055.158132001126,
            "unit": "iter/sec",
            "range": "stddev: 0.0008734036969629364",
            "extra": "mean: 71.14825679002328 usec\nrounds: 7001"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_annotation_benchmark",
            "value": 17195.100321868802,
            "unit": "iter/sec",
            "range": "stddev: 0.0008043182971587334",
            "extra": "mean: 58.156101522024606 usec\nrounds: 8244"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_benchmark",
            "value": 23761.42024521989,
            "unit": "iter/sec",
            "range": "stddev: 0.0009341046243803438",
            "extra": "mean: 42.08502647063662 usec\nrounds: 11521"
          },
          {
            "name": "tests/sql/postgres/unit/test_data_query.py::test_aggregation_join_benchmark",
            "value": 15569.511790454299,
            "unit": "iter/sec",
            "range": "stddev: 0.0009752852963486421",
            "extra": "mean: 64.22808970883096 usec\nrounds: 7592"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_create_schema_benchmark",
            "value": 13854.531833159072,
            "unit": "iter/sec",
            "range": "stddev: 0.0014256241236098993",
            "extra": "mean: 72.17854865413975 usec\nrounds: 4712"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_rename_schema_benchmark",
            "value": 52897.87280302353,
            "unit": "iter/sec",
            "range": "stddev: 0.0008812683223225204",
            "extra": "mean: 18.90435185784715 usec\nrounds: 9475"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_schema_benchmark",
            "value": 53809.06401337348,
            "unit": "iter/sec",
            "range": "stddev: 0.0008714194589116819",
            "extra": "mean: 18.58422959655021 usec\nrounds: 9606"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_property_benchmark",
            "value": 34685.437377224545,
            "unit": "iter/sec",
            "range": "stddev: 0.0011238053250035747",
            "extra": "mean: 28.830543179387117 usec\nrounds: 7864"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_property_benchmark",
            "value": 98503.88597739911,
            "unit": "iter/sec",
            "range": "stddev: 0.000008726281437389047",
            "extra": "mean: 10.151883756438213 usec\nrounds: 5042"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_update_property_benchmark",
            "value": 44891.78337371444,
            "unit": "iter/sec",
            "range": "stddev: 0.00098314393627719",
            "extra": "mean: 22.2757913552958 usec\nrounds: 8239"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_constraint_benchmark",
            "value": 33534.79414997372,
            "unit": "iter/sec",
            "range": "stddev: 0.0011296798852940529",
            "extra": "mean: 29.819774516217915 usec\nrounds: 7807"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_drop_constraint_benchmark",
            "value": 34088.505875346666,
            "unit": "iter/sec",
            "range": "stddev: 0.001059861722069282",
            "extra": "mean: 29.33540131259362 usec\nrounds: 6476"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_add_index_benchmark",
            "value": 35096.873671351386,
            "unit": "iter/sec",
            "range": "stddev: 0.0009618262581191612",
            "extra": "mean: 28.492566299894467 usec\nrounds: 7320"
          },
          {
            "name": "tests/sql/postgres/unit/test_schema_mutation.py::test_delete_index_benchmark",
            "value": 56801.583801726454,
            "unit": "iter/sec",
            "range": "stddev: 0.000011433857468498914",
            "extra": "mean: 17.605142903948494 usec\nrounds: 4111"
          }
        ]
      }
    ]
  }
}