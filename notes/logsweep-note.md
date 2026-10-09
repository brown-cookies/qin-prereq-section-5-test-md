At first I don't know what to do on this test, the condition for this is must not read on `samples/`
and must not depend on any file on my machine until I discovered the `tmp_path` for temporary files
and `capsys` for reading console output. I had to set up different fixtures to test different kind of
scenario, I can do it inside the test but I kinda enjoy using fixtures for clean `tests/test_*` setup
I tested `main` function here since testing `sweep` feels lacking.