from typing import Dict, Any, Union
import json

def merge_json(dict1: Union[Dict, str], dict2: Union[Dict, str], extend: bool = False) -> Dict[str, Any]:
    """
    Merge two JSON files or dictionaries that may contain nested dictionaries or lists
    
    Args:
        dict1: First dictionary or path to JSON file
        dict2: Second dictionary or path to JSON file
        extend: Boolean flag to determine if lists should be extended
        
    Returns:
        dict: Merged dictionary
    """
    
    def merge_lists(aList, bList, extend=False):
        """Merge two lists with option to extend"""
        if not extend:
            # Simple list merge without extension
            cLen = min(len(aList), len(bList))
            for idx in range(cLen):
                if isinstance(aList[idx], dict) and isinstance(bList[idx], dict):
                    aList[idx] = merge_dicts(aList[idx], bList[idx], extend=extend)
                elif isinstance(aList[idx], list) and isinstance(bList[idx], list):
                    aList[idx] = merge_lists(aList[idx], bList[idx], extend=extend)
                else:
                    aList[idx] = bList[idx]
            
            # Append remaining items from bList
            aList.extend(bList[cLen:])
            return aList
        else:
            # Extend lists by matching dictionary keys
            merged_list = aList.copy()
            for b_item in bList:
                if isinstance(b_item, dict):
                    found_match = False
                    for a_item in merged_list:
                        if isinstance(a_item, dict) and set(a_item.keys()) & set(b_item.keys()):
                            # Merge dictionaries with common keys
                            a_item.update(merge_dicts(a_item, b_item, extend=extend))
                            found_match = True
                            break
                    if not found_match:
                        merged_list.append(b_item)
                else:
                    if b_item not in merged_list:
                        merged_list.append(b_item)
            return merged_list

    def merge_dicts(a: Dict, b: Dict, extend: bool = False) -> Dict:
        """Merge two dictionaries recursively"""
        result = a.copy()
        
        for key, b_value in b.items():
            if key in result:
                a_value = result[key]
                if isinstance(a_value, dict) and isinstance(b_value, dict):
                    result[key] = merge_dicts(a_value, b_value, extend=extend)
                elif isinstance(a_value, list) and isinstance(b_value, list):
                    result[key] = merge_lists(a_value, b_value, extend=extend)
                else:
                    result[key] = b_value
            else:
                result[key] = b_value
                
        return result

    # Load JSON files if string paths are provided
    if isinstance(dict1, str):
        with open(dict1, 'r') as f:
            dict1 = json.load(f)
    if isinstance(dict2, str):
        with open(dict2, 'r') as f:
            dict2 = json.load(f)

    # Perform the merge
    return merge_dicts(dict1, dict2, extend=extend)