using System.Web.Mvc;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using RobotDesk.Web;
using RobotDesk.Web.Controllers;

namespace RobotDesk.Web.Tests.Controllers
{
    [TestClass]
    public class HomeControllerTest
    {
        [TestMethod]
        [Ignore]
        public void Index()
        {
            // Arrange
            HomeController controller = new HomeController();

            // Act
            ViewResult result = controller.Index() as ViewResult;

            // Assert
            Assert.IsNotNull(result);
            Assert.AreEqual("Home Page", result.ViewBag.Title);
        }
    }
}
