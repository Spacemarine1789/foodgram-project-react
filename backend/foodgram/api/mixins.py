from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST
)
from .models import User


def add_del_act(request, id, model, query, ser):
    # user = request.user
    if request.user.is_anonymous:
        return Response(status=HTTP_401_UNAUTHORIZED)
    q_obj = get_object_or_404(query, id=id)
    if query == User:
        obj = model.objects.filter(user=request.user, author=q_obj)
    else:
        obj = model.objects.filter(user=request.user, recipe=q_obj)
    if request.method == 'POST':
        if obj.exists():
            return Response(
                data='You already have this object',
                status=HTTP_400_BAD_REQUEST
            )
        if query == User:
            model.objects.create(user=request.user, author=q_obj)
        else:
            model.objects.create(user=request.user, recipe=q_obj)
        serializer = ser(q_obj)
        return Response(serializer.data, status=HTTP_201_CREATED)
    if request.method == 'DELETE':
        if not obj.exists():
            return Response(
                data='You not have this object',
                status=HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(data='Bad Requst', status=HTTP_400_BAD_REQUEST)
