from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from courseInfo.forms import InstructorForm, SectionForm, CourseForm, SemesterForm, StudentForm, RegistrationForm
from courseInfo.utils import PageLinksMixin
from .models import (
    Instructor,
    Section,
    Course,
    Semester,
    Student,
    Registration,

)


class InstructorList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):     # mixin super class
    paginate_by = 15
    model = Instructor
    permission_required = 'courseInfo.view_instructor'


class InstructorDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
        permission_required = 'courseInfo.view_instructor'

        # typically we only subclass one superclass
        def get(self, request, pk):
            # get an object or return 404
            instructor = get_object_or_404(
                Instructor,
                # pk came in
                pk=pk
            )
            # instructor is related to
            section_list = instructor.sections.all()
            # render a page, template page and context
            return render(
                request,
                # template page
                'courseInfo/instructor_detail.html',
                # context(dictionary)
                {'instructor': instructor, 'section_list': section_list}
            )


class InstructorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = InstructorForm
    model = Instructor
    permission_required = 'courseInfo.add_instructor'


class InstructorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = InstructorForm
    model = Instructor
    template_name = 'courseInfo/instructor_form_update.html'
    permission_required = 'courseInfo.change_instructor'


class InstructorDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.delete_instructor'

    def get(self, request, pk):
        instructor = self.get_object(pk)
        sections = instructor.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseInfo/instructor_refuse_delete.html',
                {'instructor': instructor,
                 'sections':sections,
                 }
            )
        else:
            return render(
                request,
                'courseInfo/instructor_confirm_delete.html',
                {'instructor': instructor}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Instructor,
            pk=pk)

    def post(self, request, pk):
        instructor = self.get_object(pk)
        instructor.delete()
        return redirect('courseInfo_instructor_list_urlpattern')


class SectionList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Section
    permission_required = 'courseInfo.view_section'


class SectionDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.view_section'

    def get(self, request, pk):
        section = get_object_or_404(
            Section,
            pk=pk
        )
        course = section.course
        semester = section.semester
        instructor = section.instructor
        registration_list = section.registrations.all()
        # 'registrations' is the related name in class Registration
        return render(
            request,
            'courseInfo/section_detail.html',
            {'section': section,
             # section
             'course': course,
             'semester': semester,
             'instructor': instructor,
             'registration_list': registration_list}
        )


class SectionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SectionForm
    model = Section
    template_name = 'courseInfo/section_form_update.html'
    permission_required = 'courseInfo.change_section'


class SectionDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.delete_section'

    def get_object(self, pk):
        return get_object_or_404(
            Section,
            pk=pk
        )

    def get(self, request, pk):
        section = self.get_object(pk)
        registrations = section.registrations.all()
        # to find section is the foreign key of which classes
        if registrations.count() > 0:
            return render(
                request,
                'courseInfo/section_refuse_delete.html',
                {
                    'section': section,
                    'registrations': registrations,
                }
            )
        else:
            return render(
                request,
                'courseInfo/section_confirm_delete.html',
                {'section': section}
            )

    def post(self, request, pk):
        section = self.get_object(pk)
        section.delete()
        return redirect('courseInfo_section_list_urlpattern')


class SectionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SectionForm
    model = Section
    permission_required = 'courseInfo.add_section'


class CourseList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    permission_required = 'courseInfo.view_course'


class CourseDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.view_course'

    def get(self, request, pk):
        course = get_object_or_404(
            Course,
            pk=pk
        )
        name = course.course_name
        number = course.course_number
        section_list = course.sections.all()
        return render(
            request,
            'courseInfo/course_detail.html',
            {'course': course,
             'name': name,
             'number': number,
             'section_list': section_list}
        )


class CourseUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = CourseForm
    model = Course
    template_name = 'courseInfo/course_form_update.html'
    permission_required = 'courseInfo.change_course'


class CourseDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.delete_course'

    def get_object(self, pk):
        return get_object_or_404(
            Course,
            pk=pk
        )

    def get(self, request, pk):
        course = self.get_object(pk)
        sections = course.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseInfo/course_refuse_delete.html',
                {
                    'course': course,
                    'sections': sections,
                }
            )
        else:
            return render(
                request,
                'courseInfo/course_confirm_delete.html',
                {'course': course}
            )

    def post(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return redirect('courseInfo_course_list_urlpattern')


class CourseCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = CourseForm
    model = Course
    permission_required = 'courseInfo.add_course'


class SemesterList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Semester
    permission_required = 'courseInfo.view_semester'


class SemesterDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.view_semester'

    def get(self, request, pk):
        semester = get_object_or_404(
            Semester,
            pk=pk
        )
        name = semester.__str__()
        section_list = semester.sections.all()
        return render(
            request,
            'courseInfo/semester_detail.html',
            {'semester': semester,
             'name': name,
             'section_list': section_list}
        )


class SemesterUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = SemesterForm
    model = Semester
    template_name = 'courseInfo/semester_form_update.html'
    permission_required = 'courseInfo.change_semester'


class SemesterDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.delete_semester'

    def get_object(self, pk):
        return get_object_or_404(
            Semester,
            pk=pk
        )

    def get(self, request, pk):
        semester = self.get_object(pk)
        sections = semester.sections.all()
        if sections.count() > 0:
            return render(
                request,
                'courseInfo/semester_refuse_delete.html',
                {
                    'semester': semester,
                    'sections': sections,
                }
            )
        else:
            return render(
                request,
                'courseInfo/semester_confirm_delete.html',
                {'semester': semester}
            )

    def post(self, request, pk):
        semester = self.get_object(pk)
        semester.delete()
        return redirect('courseInfo_semester_list_urlpattern')


class SemesterCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = SemesterForm
    model = Semester
    permission_required = 'courseInfo.add_semester'


class StudentList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    paginate_by = 25
    model = Student
    permission_required = 'courseInfo.view_student'


class StudentDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.view_student'

    def get(self, request, pk):
        student = get_object_or_404(
            Student,
            pk=pk
        )
        nickname = student.nickname
        registration_list = student.registrations.all()
        return render(
            request,
            'courseInfo/student_detail.html',
            {'student': student,
             'nickname': nickname,
             'registration_list': registration_list}
        )


class StudentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = StudentForm
    model = Student
    template_name = 'courseInfo/student_form_update.html'
    permission_required = 'courseInfo.change_student'


class StudentDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.delete_student'

    def get_object(self, pk):
        return get_object_or_404(
            Student,
            pk=pk
        )

    def get(self, request, pk):
        student = self.get_object(pk)
        registrations = student.registrations.all()
        if registrations.count() > 0:
            return render(
                request,
                'courseInfo/student_refuse_delete.html',
                {
                    'student': student,
                    'registrations': registrations,
                }
            )
        else:
            return render(
                request,
                'courseInfo/student_confirm_delete.html',
                {'student': student}
            )

    def post(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return redirect('courseInfo_student_list_urlpattern')


class StudentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = StudentForm
    model = Student
    permission_required = 'courseInfo.add_student'


class RegistrationList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Registration
    permission_required = 'courseInfo.view_registration'


class RegistrationDetail(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'courseInfo.view_registration'

    def get(self, request, pk):
        registration = get_object_or_404(
            Registration,
            pk=pk
        )
        section = registration.section
        student = registration.student
        return render(
            request,
            'courseInfo/registration_detail.html',
            {'registration': registration,
             'student': student,
             'section': section}
        )


class RegistrationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = RegistrationForm
    model = Registration
    template_name = 'courseInfo/registration_form_update.html'
    permission_required = 'courseInfo.change_registration'


class RegistrationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Registration
    success_url = reverse_lazy('courseInfo_registration_list_urlpattern')
    permission_required = 'courseInfo.delete_registration'


class RegistrationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = RegistrationForm
    model = Registration
    permission_required = 'courseInfo.add_registration'
