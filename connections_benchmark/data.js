window.BENCHMARK_DATA = {
  "lastUpdate": 1722273646564,
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
      }
    ]
  }
}