from rest_framework import generics
from memo.models import Goal
from .serializers import GoalSerializer


class Goals(generics.ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class GoalDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


# class GoalDetails(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]
#
#     def get(self, request, pk, format=None):
#         goal = Goal.objects.get(pk=pk)
#         serializer = GoalSerializer(goal)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoalSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST)
