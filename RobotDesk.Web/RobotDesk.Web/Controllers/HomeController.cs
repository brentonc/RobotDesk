using System;
using System.Linq;
using System.Web.Mvc;
using RobotDesk.Core;
using RobotDesk.Core.Services;
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
            //            model.Log = htLogSvc.GetRecentHeightLogs(10);
            //            model.CurrentHeight = model.Log.FirstOrDefault();
            model.Log = htLogSvc.GetPeriodHeightLogsPlusOneMore(new DateTime(2015, 06, 07), new DateTime(2015, 06, 07, 23, 59, 59));
            
            
            return View(model);
        }
    }
}
