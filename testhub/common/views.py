from rest_framework import generics
from rest_framework.response import Response

from testhub.common.models import Directory, Project, Requirement
from testhub.common.serializers import DirectorySerializer, ProjectSerializer, RequirementSerializer
from testhub.common.services import get_tree_root, get_node_by_id


class DirectoryAPI(generics.GenericAPIView):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

    def get(self, request):
        queryset = get_tree_root(self.queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class DirectoryDetailAPI(generics.GenericAPIView):
    queryset = Directory.objects.all()
    serializer_class = DirectorySerializer

    def get(self, request, pk):
        queryset = get_node_by_id(self.get_queryset(), pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        serializer = self.get_serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        queryset = self.get_queryset().filter(id=pk)
        queryset.delete()
        return Response(status=204)


class ProjectAPI(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProjectDetailAPI(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        serializer = self.get_serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        queryset.delete()
        return Response(status=204)


class RequirementAPI(generics.GenericAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=request.data["project_id"])
            return Response(serializer.data)
        return Response(serializer.errors)


class RequirementDetailAPI(generics.GenericAPIView):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

    def get(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        serializer = self.get_serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        queryset = self.get_queryset().filter(id=pk).first()
        queryset.delete()
        return Response(status=204)
