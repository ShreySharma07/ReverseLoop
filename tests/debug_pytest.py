def test_debug_path():
    import sys
    print("\n=== PYTHONPATH ===")
    for p in sys.path:
        print(p)
