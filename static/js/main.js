document.addEventListener('DOMContentLoaded', function() {
  const currentLocation = window.location.pathname;
  const navLinks = document.querySelectorAll('header nav a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentLocation || 
        (href !== '/' && currentLocation.startsWith(href))) {
      link.classList.add('active');
    }
  });

  if (typeof bootstrap !== 'undefined') {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl);
    });

    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
      new bootstrap.Popover(popoverTriggerEl);
    });
  }

  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });

  const selectAllCheckbox = document.getElementById('selectAll');
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', function() {
      const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
      checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
      });
    });
  }

  const chartContainers = document.querySelectorAll('.chart-container');
  if (chartContainers.length > 0) {
    console.log('Chart containers found. Would initialize charts here in a real app.');
  }

  const animateOnScroll = () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
      const cardPosition = card.getBoundingClientRect();
      if (cardPosition.top < window.innerHeight && cardPosition.bottom > 0) {
        card.classList.add('animate');
      }
    });
  };

  window.addEventListener('scroll', animateOnScroll);
  animateOnScroll();

  // ✅ Load default dashboard on page load
  loadDashboard('employee');
});

window.loadDashboard = function(type) {
  const dashboards = {
    employee: { title: "Employee Insights", url: "https://app.powerbi.com/view?r=eyJrIjoiZDA1YzFlNDMtZGVhZC00OGNlLTk5ZTItMDUxNzc2ZTBhZDdjIiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9&pageName=921fea38dd028eaa06d6" },
    absence: { title: "Absence Insights", url: "https://app.powerbi.com/view?r=eyJrIjoiZDA1YzFlNDMtZGVhZC00OGNlLTk5ZTItMDUxNzc2ZTBhZDdjIiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9&pageName=178bad63bacb0b9bdc0a" },
    attrition: { title: "Attrition Insights", url: "https://app.powerbi.com/view?r=ATTRITION_DASHBOARD_URL" },
  };

  const iframe = document.getElementById("powerbiFrame");
  const loading = document.getElementById("loadingSection")
  const title = document.getElementById("dashboardTitle");

  if (!dashboards[type]) return;

  title.innerText = dashboards[type].title;
  iframe.style.display = "none";
  loading.style.display = "block";
  iframe.src = dashboards[type].url;

  iframe.onload = function () {
    loading.style.display = "none";
    iframe.style.display = "block";
  };
};