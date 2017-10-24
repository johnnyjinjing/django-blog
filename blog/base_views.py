from django.shortcuts import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.utils.html import escape

class PaginatedListView(ListView):
    """ Paginated ListView
    """
    N_PAGE_ONESIDE = 2
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PaginatedListView, self).get_context_data(**kwargs)

        # get context provided in ListView
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # get pagination data
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        """
        get custormized pagination data
        For example: page = [1, 2, 3, ..., 9], current_page = 7, NPAGE = 2
            then left = [5, 6], right = [8, 9], left_has_more = True,
            right_has_more = False, first = True, last = False
        """
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False # if ellipses is needed on the left
        right_has_more = False # if ellipses is needed on the right
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = list(paginator.page_range)

        if page_number == 1: # first page, left = [], left_has_more = False, first = False
            if 1 + self.N_PAGE_ONESIDE < len(page_range):
                right = page_range[1:1 + self.N_PAGE_ONESIDE]
            else:
                right = page_range[1:]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages: # last page, right = [], right_has_more = False, last = False
            if page_number - self.N_PAGE_ONESIDE - 1 > 0:
                left = page_range[page_number - self.N_PAGE_ONESIDE - 1:page_number - 1]
            else:
                left = page_range[:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            if page_number - self.N_PAGE_ONESIDE - 1 > 0:
                left = page_range[page_number - self.N_PAGE_ONESIDE - 1:page_number - 1]
            else:
                left = page_range[:page_number - 1]

            if page_number + self.N_PAGE_ONESIDE < len(page_range):
                right = page_range[page_number:page_number + self.N_PAGE_ONESIDE]
            else:
                right = page_range[page_number:]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

class MiscCreateMixin(CreateView):
    """ View used to add misc infomation on the fly
    """
    def form_valid(self, form):
            obj = form.save()
            pk_value = obj.pk

            if "_popup" in self.request.GET:
                return HttpResponse('''
                    <script>opener.closeAddPopup(window,
                    "%s", "%s", "%s");</script>
                ''' % (escape(pk_value), escape(obj),
                    escape(self.request.GET.get('_to_field'))))

            return super(CreateMixin, self).form_valid(form)
