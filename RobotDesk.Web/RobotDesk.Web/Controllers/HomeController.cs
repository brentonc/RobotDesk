using System.Linq;
using System.Web.Mvc;
using RobotDesk.Core;
using RobotDesk.Web.Models;

namespace RobotDesk.Web.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            ViewBag.Title = "Home Page";
            var model = new HomeViewModel();
            var htLogSvc = new HeightLogSvc();
            model.Log = htLogSvc.GetRecentHeightLogs(10);
            model.CurrentHeight = model.Log.FirstOrDefault();
            
            return View(model);
        }
    }
}
