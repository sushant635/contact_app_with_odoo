from django.shortcuts import render,get_object_or_404
import xmlrpc.client
from django.http import HttpResponse
# import xmlrpclib
# Create your views here.
import json
from contact.models import Contact
import sys


url = 'http://localhost:8069/'
db = 'demodata'
username = 'admin'
password = 'admin'

# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# version = common.version()
# print('details..',version)

# info = xmlrpc.client.ServerProxy('http://localhost:8069/start').start()
common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common')
output = common.version()
print('details..',output)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object')

# partner = models.execute_kw(db, uid, password,
#     'res.partner',['read'], {'raise_exception': False})

partner = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]])


partnerlimit = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]],
    {'offset': 10, 'limit': 5})


partnercount = models.execute_kw(db, uid, password,
    'res.partner', 'search_count',
    [[['is_company', '=', True]]])


ids = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]],)
# [record] = models.execute_kw(db, uid, password,
#     'res.partner', 'read', [ids])

# print(len(record))
# print('id..',id)
# print('record',[record])
partnerdata = models.execute_kw(
    db, uid, password, 'res.partner', 'fields_get',
    [], {'attributes': ['string', 'help', 'type']})

partnerdetails = models.execute_kw(db, uid, password,
    'res.partner', 'read',
    [ids], {'fields': ['name', 'country_id', 'comment','city','company_name','contact_address','category_id','user_id','parent_id','display_name','title',
    'email','phone','mobile',]})

# print('partner details...',partnerdetails)
# print('partner',partner)
# print('partner limit ..',partnerlimit)
# print('partner count..',partnercount)
for i in partnerdetails:
    print('Details..',i)



# print(partnerdata)


def contact_details(request):
    if request.method == 'GET':
        try:
            partnerdetails = models.execute_kw(db, uid, password,
            'res.partner', 'read',
            [ids], {'fields': ['name', 'country_id', 'comment','city','company_name','contact_address','category_id','user_id','parent_id','display_name','title',
            'email','phone','display_name','id','image_1920','child_ids']})

        
            for i in partnerdetails:
                # print(i['id'],i['display_name'])
                if Contact.objects.filter(contact=i['id'],display_name=i['display_name']).exists():
                    # print('data created')
                    pass
                else:
                    data = Contact.objects.create(contact_id=i['id'],display_name=i['display_name'])
                    data.save()
            # print('details',partnerdetails)
            return render(request,'contact.html',{'contact':partnerdetails})

        except Exception as error:
            print(error,'Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
            return HttpResponse('error',error)

    if request.method == 'POST':
        try:
            print(request.POST)

        except Exception as e:
            print(e,'line number of error'.format(sys.exc_info()[-1].tb_lineno))


def details(request, contact_id):
    try:
        print('contact details',contact_id)
        ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['id', '=', contact_id]]],)
        print('ids are correcte',ids)
        partnerdetails = models.execute_kw(db, uid, password,
            'res.partner', 'read',
            [ids], {'fields': ['name', 'country_id', 'comment','city','company_name','contact_address','category_id','user_id','parent_id','display_name','title',
            'email','phone','display_name','id','image_1920','child_ids','mobile','website','vat']})
        print(partnerdetails)
        
        child_id_list = []
        cotegory_id = []
        for i in partnerdetails:
            # print(i['child_ids'])
            temp = i['child_ids']
            print('temp',temp)
            tmp = i['category_id']
            child_id_list.append(temp)
            cotegory_id.append(tmp)
        print('child id list',child_id_list)
        

        child_details = []
        print(len(child_id_list))
        print(type(child_id_list))
        for child in child_id_list:
            print('child ids in for loop',child)
            for i in child:
                print(i)
                child_ids = models.execute_kw(db, uid, password,
                'res.partner', 'search',
                 [[['id', '=',i]]],)
                # print(child_ids)

                partnerdetails3 = models.execute_kw(db, uid, password,
                'res.partner', 'read',
                [child_ids], {'fields': ['name', 'country_id', 'comment','city','company_name','contact_address','category_id','user_id','parent_id','display_name','title',
                'email','phone','display_name','id','function','comment','mobile']})

                child_details.append(partnerdetails3)

       
            # category = models.execute_kw(db, uid, password,
            # 'res.partner.category', 'read',
            # [category], {'fields': ['name']})
            # print(category)
        cotegory_name = []
        print(cotegory_id)
        for i in cotegory_id:
            for j in i:
                cot_id = models.execute_kw(db, uid, password,
                'res.partner.category', 'search',
                 [[['id', '=',j]]],)
                name = models.execute_kw(db, uid, password,
                'res.partner.category', 'read',
                [cot_id], {'fields': ['name']})
                # print()
                cotegory_name.append(name)
                

        print('child details',child_details)

        context = {'child':child_details,'parent':partnerdetails,'cotegory':cotegory_name}

        # contact = get_object_or_404(Contact,contact=contact_id)
        # print('conatct objects',contact)

        # return HttpResponse("working",contact_id)
        return render(request, 'contact_detail.html',context)
    except Exception as error:
        print(error,'line number of error'.format(sys.exc_info()[-1].tb_lineno))



# def child_details(request):
#     if request.method == "POST":
#         print(request.POST)

#         id = request.POST.get()


