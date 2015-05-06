require 'socket'

  

receive_server = TCPServer.new('', 25000)

send_server = TCPServer.new('', 26000)

connections = []



Thread.new{

  while (session = receive_server.accept)

    connections << session

  end

}



Thread.new{

  while (session = send_server.accept)

    request = session.gets

    connections.each{|c|

      begin

        c.write(request)

      rescue Errno::EPIPE

        connections.delete(c)

      end

    }

    session.close

  end

}.join
