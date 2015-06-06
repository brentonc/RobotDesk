using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
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
//            var _serviceBusConn = Environment.GetEnvironmentVariable("SQLAZURECONNSTR_servicebus")

            JobHostConfiguration config = new JobHostConfiguration();
            config.DashboardConnectionString = null;
//            config.ServiceBusConnectionString = "Endpoint=sb://brentoniot-ns.servicebus.windows.net/;SharedAccessKeyName=ReadPolicy;SharedAccessKey=lNx8LvT1dUwi3y8Uz1kfHc5uygf35unsPo/B5CD6vQE=";
            var host = new JobHost(config);
            // The following code ensures that the WebJob will be running continuously
//            var host = new JobHost();
            host.RunAndBlock();
        }
    }
}
