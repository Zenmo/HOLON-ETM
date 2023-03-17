config_dict = {
    "module": "upscaling",
    "name": "National upscaling",
    "api_url": "https://beta-engine.energytransitionmodel.com/api/v3/scenarios/",
    "etm_scenario_id": 2171095,
    "config": {
        "households_solar_pv_solar_radiation": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "households_solar_pv_solar_radiation_market_penetration"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.301,
                    "key": "scaling_buurtelektrificatie"
                }
            ]
        },
        "households_flexibility_p2p_electric": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "households_flexibility_p2p_electricity_market_penetration"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.301,
                    "key": "share_of_households_batteries"
                }
            ]
        },
        "households_cooker_induction_electri": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "households_cooker_induction_electricity_share"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.301,
                    "key": "share_of_households_induction_cooking"
                }
            ]
        },
        "shadow_mv_batteries": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "capacity_of_energy_flexibility_mv_batteries_electricity"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 50.0,
                    "key": "installed_energy_grid_battery"
                }
            ]
        },
        "share_of_electric_trucks_shadow": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "share_of_electric_trucks"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.6,
                    "key": "scaling_buurtelektrificatie"
                },
                {
                    "type": "query",
                    "etm_key": "Tester_convert_with_etm",
                    "value_type": "value",
                    "conversion": "multiply"
                },
                {
                    "type": "static",
                    "type_actual": "datamodel",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 200.0,
                    "key": "truck_conversion"
                }
            ]
        },
        "shadow_key_households": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "households_heater_heatpump_air_water_electricity_share"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.301,
                    "key": "share_of_households_heat_pumps"
                }
            ]
        },
        "households_heater_hybrid_heatpump": {
            "value": {
                "type": "input",
                "data": "value",
                "etm_key": "households_heater_hybrid_heatpump_air_water_electricity_share"
            },
            "convert_with": [
                {
                    "type": "static",
                    "type_actual": "static - local variable",
                    "conversion": "multiply",
                    "data": "value",
                    "value": 0.301,
                    "key": "share_of_households_hybrid_heat_pumps"
                }
            ]
        }
    }
}
