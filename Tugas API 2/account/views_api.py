from django.shortcuts import render, redirect
from django.http import HttpResponse
from account.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
import requests
import logging
import urllib.parse

        # Command CMD
            # <!Get!>
            # curl http://127.0.0.1:8000/api/course/
            # <!POST!>
            # curl -X POST -H "Content-Type: application/json" -d '{"course_name":"example_course"}' http://127.0.0.1:8000/api/course/
            # <!PUT!>
            # curl -X PUT -H "Content-Type: application/json" -d '{"course_name":"name course", "new_course_name":"Updated Course Name"}' http://127.0.0.1:8000/api/course/
            # <!DELETE!>
            # curl -X DELETE -H "Content-Type: application/json" -d '{"course_name":"Updated Course Name"}' http://127.0.0.1:8000/api/course/

@csrf_exempt
def apiCourse(request):
    if (request.method == "GET"):
        # Serialize the data into json
        data = serializers.serialize("json", Course.objects.all())
        # Turn the JSON data into a dict and send as JSON response
        return JsonResponse(json.loads(data), safe=False)

    if (request.method == "POST"):
        # Turn the body into a dict
        body = json.loads(request.body.decode("utf-8"))
        # filter data
        if not body:
            data = '{"message": "data is not json type!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        else:
            created = Course.objects.create(
                course_name=body['course_name']
            )
            data = '{"message": "data successfully created!"}'
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)

    if (request.method == 'PUT'):
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

        if 'course_name' not in body:
            return JsonResponse({'message': 'Missing course name'}, status=400)

        try:
            course = Course.objects.get(course_name=body['course_name'])
        except Course.DoesNotExist:
            return JsonResponse({'message': 'Course not found'}, status=404)

        course.course_name = body.get('course_name', course.course_name)
        course.save()
        return JsonResponse({'message': 'Course successfully updated!', 'course_name': course.course_name})

    if (request.method == 'DELETE'):
        try:
            body = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

        if 'course_name' in body:
            try:
                course = Course.objects.get(course_name=body['course_name'])
            except Course.DoesNotExist:
                return JsonResponse({'message': 'Course not found'}, status=404)
        else:
            try:
                course = Course.objects.latest('course_created_date')
            except Course.DoesNotExist:
                return JsonResponse({'message': 'No courses found'}, status=404)

        course.delete()
        return JsonResponse({'message': 'Course successfully deleted!'})

# @csrf_exempt
# def consumeApiGet(request):
#     response = requests.get("https://jsonplaceholder.typicode.com/users")
#     data = response.json()
#     return render(request, 'api-get.html', {'data':data})


@csrf_exempt
def consumeApiGet(request):
    data = request.GET
    return render(request,'post-output.html', {'data':data})
@csrf_exempt
def consumeApiPost(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            body = request.POST.get("body")
            userId = request.POST.get("userId")

            if not title or not body or not userId:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            api_url = "https://jsonplaceholder.typicode.com/posts"
            payload = {
                "title": title,
                "body": body,
                "userId": userId
            }

            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            data = response.json()

            query_string = urllib.parse.urlencode(data)
            return redirect(f'{request.build_absolute_uri("/api/consume/course/")}?{query_string}')
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'new-post.html')


