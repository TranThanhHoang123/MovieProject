from rest_framework.response import Response
from rest_framework import generics, status


class ListApiViewFilterByName(generics.ListAPIView):
    queryset = None
    serializer_class = None

    # tìm theo tên
    def get_queryset(self):
        query = self.queryset
        kw = self.request.query_params.get('name')
        if kw:
            query = query.filter(name__icontains=kw)
        return query


class UpdateAPIView(generics.UpdateAPIView):
    queryset = None
    serializer_class = None

    # tìm theo tên
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
