class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

def tapisresult_to_json_serializer(result):
        if type(result) in [str, int, float, type(None), bool]: return result
        
        if type(result) == list:
            modified_result = []
            for res in result:
                modified_result.append(tapisresult_to_json_serializer(res))

            return modified_result
        
        modified_result = result.__dict__
        for prop in modified_result:
            modified_result[prop] = tapisresult_to_json_serializer(modified_result[prop])

        return modified_result