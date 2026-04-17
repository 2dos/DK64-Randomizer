#!/usr/bin/env python3
"""Test protobuf serialization of Fill results."""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from randomizer.proto_gen import fill_result_pb2


def test_basic_serialization():
    """Test basic fill result protobuf structure."""
    print("Testing FillResult protobuf serialization...")
    
    # Create a minimal FillResult proto directly
    try:
        fill_result = fill_result_pb2.FillResult()
        
        # Test location assignments
        fill_result.location_assignments.assignments[1] = 100
        fill_result.location_assignments.assignments[2] = 101
        print(f"✓ Created location assignments")
        
        # Test CB placement
        cb = fill_result.placement_data.cb_placements.add()
        cb.id = 1
        cb.name = "Test CB Group"
        cb.kong = 1  # DK
        cb.level = 1  # Japes
        cb.type = "cb"
        cb.map = 7
        print(f"✓ Created CB placement")
        
        # Test move shop data
        shop_type = fill_result.move_shop_data.shop_types.add()
        print(f"✓ Created shop type")
        
        # Test serialization to bytes
        proto_bytes = fill_result.SerializeToString()
        print(f"✓ Serialized to {len(proto_bytes)} bytes")
        
        # Test deserialization
        fill_result2 = fill_result_pb2.FillResult()
        fill_result2.ParseFromString(proto_bytes)
        print(f"✓ Deserialized successfully")
        
        # Verify data
        assert len(fill_result2.location_assignments.assignments) == 2
        assert fill_result2.location_assignments.assignments[1] == 100
        assert len(fill_result2.placement_data.cb_placements) == 1
        assert fill_result2.placement_data.cb_placements[0].name == "Test CB Group"
        print(f"✓ Data integrity verified")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_basic_serialization()
    sys.exit(0 if success else 1)
