using Microsoft.Azure.WebJobs;

namespace RobotDesk.QueueReaderJob
{
    // To learn more about Microsoft Azure WebJobs SDK, please see http://go.microsoft.com/fwlink/?LinkID=320976
    class Program
    {
        // Please set the following connection strings in app.config for this WebJob to run:
        // AzureWebJobsDashboard and AzureWebJobsStorage
        static void Main()
        {
            var config = new JobHostConfiguration {DashboardConnectionString = null};
            var host = new JobHost(config);
            host.RunAndBlock();
        }
    }
}
