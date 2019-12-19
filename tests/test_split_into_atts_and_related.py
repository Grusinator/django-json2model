import django
from django.test import TransactionTestCase

from json2model.services.dynamic_model.i_json_iterator import IJsonIterator


class TestSplitIntoAttsAndRelated(TransactionTestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSplitIntoAttsAndRelated, cls).setUpClass()
        django.setup()

    def test_split(self):
        data = {
            "resource_state": 2,
            "athlete": {
                "id": 465645,
                "resource_state": 1
            },
            "name": "Morning Run",
            "distance": 5618.2,
            "moving_time": 1571,
            "elapsed_time": 1778,
            "total_elevation_gain": 12.0,
            "type": "Run",
            "workout_type": None,
            "id": 2880383294,
            "external_id": "shealth12730eee-26b1-6297-9291-f488c87dd8ef.tcx",
            "upload_id": 3058114478,
            "start_date": "2019-11-21T07:34:40Z",
            "start_date_local": "2019-11-21T08:34:40Z",
            "timezone": "(GMT+01:00) Europe/Copenhagen",
            "utc_offset": 3600.0,
            "start_latlng": [
                55.61765,
                12.434259
            ],
            "end_latlng": [
                55.61774,
                12.434354
            ],
            "location_city": None,
            "location_state": None,
            "location_country": "Denmark",
            "start_latitude": 55.61765,
            "start_longitude": 12.434259,
            "achievement_count": 0,
            "kudos_count": 1,
            "comment_count": 0,
            "athlete_count": 1,
            "photo_count": 0,
            "map": {
                "id": "a2880383294",
                "summary_polyline": "iymrIaq{jAW`@b@{@JKFDNVRl@?x@ZRbBZX@`AE\\DVVZd@Lj@UhDQdBGhBIv@Mx@Hf@ZH|@EXCZQ|@Qp@HtA?xAC`@?^E`@B^bBDt@IfHSrEU~DOrECtEG~B?xCI|BSp@Cz@F~@?vBM|F?tCIlG@z@N~DDzBApA]tFCp@?vDBzFP|H@jLHfCLhH\\rJ@~@^~Hh@hFBv@]lBOn@m@B}@Ge@v@kA~C{BvESK{A_GMm@Iq@Eu@K{@o@wEMu@SyBMuDGy@_@eDYuBI{@K{BA{@@gDHeFAgHLyCBeB?_IHwCAo@DiB@uRTwFHoI?s@FiBCuCB}Ad@i@JYLmANsJAs@WyAIo@Gm@O{BFaBXwCFgB?cDFcBBgBMoC@s@NmBF_ADoCVyD@q@Me@o@q@WGYAWF[AuAGm@KYUK_@OmAMHKMW@JSAHED",
                "resource_state": 2
            },
            "trainer": False,
            "commute": False,
            "manual": False,
            "private": False,
            "visibility": "everyone",
            "flagged": False,
            "gear_id": None,
            "from_accepted_tag": False,
            "upload_id_str": "3058114478",
            "average_speed": 3.576,
            "max_speed": 5.9,
            "average_cadence": 84.8,
            "has_heartrate": True,
            "average_heartrate": 109.3,
            "max_heartrate": 142.0,
            "heartrate_opt_out": False,
            "display_hide_heartrate_option": True,
            "elev_high": 3.0,
            "elev_low": -2.5,
            "pr_count": 0,
            "total_photo_count": 0,
            "has_kudoed": False
        }

        atts, one2one_rel_objs, one2many_rel_objs = IJsonIterator._split_into_attributes_and_related_objects(data)
        expected_atts = {}
        expected_one2one_rel_objs = {}
        expected_one2many_rel_objs = {}
        self.assertDictEqual(atts, expected_atts)
        self.assertDictEqual(one2one_rel_objs, expected_one2one_rel_objs)
        self.assertDictEqual(one2many_rel_objs, expected_one2many_rel_objs)
