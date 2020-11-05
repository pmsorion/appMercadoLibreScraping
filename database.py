from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://giftubackend.herokuapp.com/api")

class database:
    # Instantiate the client with an endpoint.
    def conect_graphql(idUser):
        query = """
                query GetSocialNetwork($id:ID!){
                social_network(id:$id){
                        receiver_name
                        social_network_name
                        url_social_network
                }
            }
        """
        variables = {"id": idUser}

        # Synchronous request
        data = client.execute(query=query, variables=variables)

        #print(data['data']['social_network']['url_social_network'])
        id_user_facebok = data['data']['social_network']['url_social_network']
        return id_user_facebok

    def podium_graphql(data_podium):
        mutation = """
                mutation AddPodium($podium:JSON!){
                PodiumMutation(podium:$podium){
                    podium
                }
            }
        """
        variables = {"podium":data_podium}
        dataResponse = client.execute(query=mutation, variables=variables)
        return dataResponse

    def search_result_graphql(task_id, data):
        mutation_result = """
                mutation AddSocialNetwrok(
                $id_pv_social_network:ID!,
                $search_result:JSON!,
                ){
                updateSocialNetwork(
                        id_pv_social_network:$id_pv_social_network,
                        search_result:$search_result,
                ){
                    id_pv_social_network
                    search_result
                }
            }
            """

        variables_result = { "id_pv_social_network": task_id, "search_result": data }

        dataResult = client.execute(query=mutation_result, variables=variables_result)
        return dataResult