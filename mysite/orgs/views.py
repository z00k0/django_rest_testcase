from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Client, Organization, Bill
from .serializers import ClientSerializer, BillSerializer
from .utils import xlsx_parse


class ClientListView(APIView):

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class BillListView(APIView):

    def get(self, request):
        bills = Bill.objects.all()
        client_id = self.request.GET.get('client_id', None)
        org_id = self.request.GET.get('org_id', None)
        if org_id:  # Фильтрация по id организации
            bills = bills.filter(organization=org_id)
        if client_id:  # Фильтрация по id клиента
            orgs = Organization.objects.filter(client_name=client_id)
            bills = bills.filter(organization__in=orgs)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    def put(self, request):
        file_obj = request.FILES['file']
        message = {}
        if file_obj:
            d = xlsx_parse(file=file_obj)  # Получаю словарь с данными из xlsx файла
            client_list = d.get('client')
            orgs_dict = d.get('organization')
            bills_dict = d.get('bills')
            if client_list:
                for client in client_list:  # сохраняю в базу каждого клиента из списка, если список не пустой
                    new_client = Client(name=client)
                    try:
                        new_client.save()
                        message[client] = 'Saved successfully'
                    except Exception as e:
                        message[client] = e.args
            if orgs_dict:
                for client in orgs_dict:  # сохраняю в базу каждую организацию из словаря, если словарь не пустой
                    _client = Client.objects.get(name=client)
                    for org in orgs_dict[client]:
                        new_org = Organization(client_name=_client, organization=org)
                        try:
                            new_org.save()
                            message[org] = 'Saved successfully'
                        except Exception as e:
                            message[org] = e.args
            if bills_dict:
                for org_name in bills_dict:  # сохраняю в базу каждый счет из словаря, если словарь не пустой
                    bills = bills_dict[org_name]
                    org = Organization.objects.get(organization=org_name)
                    for bill in bills:
                        new_bill = Bill(
                            organization=org,
                            number=bill[0],
                            amount=bill[1],
                            date=bill[2].date()
                        )
                        _bill_string = f'{org_name}, # {bill[0]}'
                        try:
                            new_bill.save()
                            message[_bill_string] = 'Saved successfully'
                        except Exception as e:
                            message[_bill_string] = e.args

        return Response(message)
