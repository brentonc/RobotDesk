using System.Web.Mvc;
using RobotDesk.Core;

namespace RobotDesk.Web.Controllers
{
    public class LogController : Controller
    {
        // GET: Log
        public ActionResult Index()
        {
            var htLogSvc = new HeightLogSvc();
            return View(htLogSvc.GetRecentHeightLogs(100));
        }
    }
}