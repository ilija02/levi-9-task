import unittest
from app.app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_player_stats(self):
        response = self.app.get('/stats/player/Sifiso%20Abdalla/')
        data = response.get_json()

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the response has the expected structure
        self.assertTrue("playerName" in data)
        self.assertTrue("gamesPlayed" in data)
        self.assertTrue("traditional" in data)
        self.assertTrue("freeThrows" in data["traditional"])
        self.assertTrue("twoPoints" in data["traditional"])
        self.assertTrue("threePoints" in data["traditional"])
        self.assertTrue("points" in data["traditional"])
        self.assertTrue("rebounds" in data["traditional"])
        self.assertTrue("blocks" in data["traditional"])
        self.assertTrue("assists" in data["traditional"])
        self.assertTrue("steals" in data["traditional"])
        self.assertTrue("turnovers" in data["traditional"])
        self.assertTrue("advanced" in data)
        self.assertTrue("valorization" in data["advanced"])
        self.assertTrue("effectiveFieldGoalPercentage" in data["advanced"])
        self.assertTrue("trueShootingPercentage" in data["advanced"])
        self.assertTrue("hollingerAssistRatio" in data["advanced"])

        # Check if the response has the expected values
        self.assertEqual(data["playerName"], "Sifiso Abdalla")
        self.assertEqual(data["gamesPlayed"], 3)

        # Traditional stats assertions
        self.assertEqual(data["traditional"]["freeThrows"]["attempts"], 4.7)
        self.assertEqual(data["traditional"]["freeThrows"]["made"], 3.3)
        self.assertEqual(data["traditional"]["freeThrows"]["shootingPercentage"], 71.4)

        self.assertEqual(data["traditional"]["twoPoints"]["attempts"], 4.7)
        self.assertEqual(data["traditional"]["twoPoints"]["made"], 3.0)
        self.assertEqual(data["traditional"]["twoPoints"]["shootingPercentage"], 64.3)

        self.assertEqual(data["traditional"]["threePoints"]["attempts"], 6.3)
        self.assertEqual(data["traditional"]["threePoints"]["made"], 1.0)
        self.assertEqual(data["traditional"]["threePoints"]["shootingPercentage"], 15.8)

        self.assertEqual(data["traditional"]["points"], 12.3)
        self.assertEqual(data["traditional"]["rebounds"], 5.7)
        self.assertEqual(data["traditional"]["blocks"], 1.7)
        self.assertEqual(data["traditional"]["assists"], 0.7)
        self.assertEqual(data["traditional"]["steals"], 1.0)
        self.assertEqual(data["traditional"]["turnovers"], 1.3)

        # Advanced stats assertions
        self.assertEqual(data["advanced"]["valorization"], 11.7)
        self.assertEqual(data["advanced"]["effectiveFieldGoalPercentage"], 40.9)
        self.assertEqual(data["advanced"]["trueShootingPercentage"], 46.7)
        self.assertEqual(data["advanced"]["hollingerAssistRatio"], 4.4)


    def test_invalid_player_name(self):
        response = self.app.get('/stats/player/InvalidPlayerName/')
        data = response.get_json()

        # Check if the response indicates player not found (status code 404)
        self.assertEqual(response.status_code, 404)
        self.assertTrue("error" in data)
        self.assertEqual(data["error"], "Player not found")

if __name__ == '__main__':
    unittest.main()
