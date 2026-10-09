I thought on mocking, I'll only mock the fetch so it took me a long time how will I write the test_shipments_*
I don't know if I'm gonna based the test on the API or just create a fixture but I went straight to the fixture
as it is more clean and satisfied `your suite must pass with the depot server not running`. There's two test
failing due to one of examples weight_kg being set to `True`. But that is a boolean not on int/float, it should be
excluded not included.
